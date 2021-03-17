#!/bin/bash -e
python3 setup.py check
python3 setup.py build
# sudo python3 setup.py install --force --install-dir /Users/yu/Library/Python/3.8/lib/python/site-packages
sudo python3 setup.py sdist bdist_wheel || true
sudo python3 -m twine upload dist/*.whl

sudo rm -rf build
sudo rm -rf dist
sudo rm -rf iotedge_application_link_sdk.egg-info

