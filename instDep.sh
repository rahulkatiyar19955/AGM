#!/usr/bin/sh


sudo apt-get install python-pyparsing python-pyside pyside-tools libpython2.7-dev python-dev libboost-all-dev cmake python-imaging python-numpy pypy cython libgsl-dev libopenscenegraph-dev
sudo apt-get install pypy-setuptools python-setuptools
sudo apt-get install libxml2-dev



git clone https://github.com/eleme/thriftpy.git
cd thriftpy
sudo pypy setup.py install
sudo make clean
sudo python setup.py install


