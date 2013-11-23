#!/bin/sh

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:.

# Ask for RoboComp support

cmake .
make agm
sudo make install
