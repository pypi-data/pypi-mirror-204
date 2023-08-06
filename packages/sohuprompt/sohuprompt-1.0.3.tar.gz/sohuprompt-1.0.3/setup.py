from distutils.core import setup
from setuptools import find_packages

setup(name='sohuprompt',
        version='1.0.3',
        packages=find_packages(),  # 查找包的路径
        # package_dir={'': 'src'},  # 包的root路径映射到的实际路径
        # include_package_data=False,
        # package_data={'data': []},
        description='A python lib for sohuprompt',
        # long_description='',
        author='senhaowang,chencheng',
        author_email='senhaowang@sohu-inc.com',
        # url='http://www.xxxxx.com/',  # homepage
        license='MIT',
        install_requires=['transformers', 'torch', 'numpy', 'pandas', 'tqdm', 'sklearn', 'jieba'],
        )