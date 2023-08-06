from distutils.core import setup
from setuptools import find_packages

setup(name='remote-drawing-provider',
    version='0.0.3',
    description='创建首个可用版本',
    author='XiaoyanQian',
    author_email='thinkershare@163.com',
    url='https://github.com/XiaoyanQian/remote-drawing',
    packages = find_packages('src'),
    package_dir = {'':'src'},
)
