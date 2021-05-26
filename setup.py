import sys

from setuptools import setup

if not (sys.version_info[0] == 3):
    sys.exit("Link IoT Edge only support Python 3")

setup(
    name='iotedge_application_link_sdk',
    version='0.1.0',
    author='ucloud.cn',
    url='https://pypi.org/project/iotedge_application_link_sdk/',
    author_email='joy.zhou@ucloud.cn',
    packages=['iotedgeapplicationlinksdk'],
    platforms="any",
    license='Apache 2 License',
    install_requires=[
        "asyncio-nats-client>=0.10.0",
        "cachetools>=4.0.0"
    ],
    description="IoT Stack Edge application Link SDK",
    long_description="IoT Stack Edge application Link SDK\n https://www.ucloud.cn/site/product/uiot.html"
)
