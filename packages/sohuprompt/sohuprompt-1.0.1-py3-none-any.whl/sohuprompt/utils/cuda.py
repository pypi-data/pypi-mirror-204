import torch
from SohuPrompt.utils.logging import logger

def model_to_device(model, config):
    r"""
    model: the model to be wrapped
    config: the environment subconfig.
    """
    import os
    if "CUDA_VISIBLE_DEVICES" not in os.environ and config.environment.cuda_visible_devices is not None:
        os.environ["CUDA_VISIBLE_DEVICES"] = ",".join([str(i) for i in config.environment.cuda_visible_devices])
    if config.environment.model_parallel: # currently not support dataparallel and model parallel simultaneously. 
        if hasattr(model, "parallelize"):
            if config.environment.device_map is None:
                model.parallelize()
            else:
                model.parallelize(config.environment.device_map)
            logger.info("Using model parallel, spread across device map: {}".format(model.device_map))
            return model
        else:
            raise RuntimeError("The model doesn't has parallelize method.")
    if config.environment.num_gpus>1 and not config.onnx.refer:
        local_rank_device = "cuda:{}".format(config.environment.local_rank)
        model = model.to(local_rank_device)
        model = torch.nn.parallel.DataParallel(model, output_device=local_rank_device)
        logger.info("Using DataParallel")
    elif config.environment.num_gpus>0 and not config.onnx.infer:
        model = model.cuda()
        logger.info("Using cuda of single gpu")
    elif config.onnx.infer:
        logger.info("Using onnx inference")
    else:
        logger.info("Using cpu")
    return model
