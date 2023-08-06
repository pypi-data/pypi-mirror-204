from distutils.core import  setup
import setuptools
packages = ['connectCode']# 唯一的包名，自己取名
setup(name='connectCode',
	version='1.0',
	author='SiriBen',
    packages=packages, 
    package_dir={'requests': 'requests'},)