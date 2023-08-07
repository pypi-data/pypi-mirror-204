from distutils.core import  setup
import setuptools
packages = ['graph2topictm']# 唯一的包名，自己取名
setup(name='graph2topictm',
	version='2.0',
    description='G2T is a topic model based on PLMs and community detections. more details in https://github.com/lunar-moon/Graph2Topic.git',
	author='Jiapeng Liu',
    author_email='liujiapeng36@fox.mail',
    packages=setuptools.find_packages()
    )
