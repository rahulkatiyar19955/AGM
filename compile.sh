# Slice files
cd RoboCompAGMExecutive/Slice
cmake .
sudo make install
cd ../..

# Library
cmake .
make
sudo make install

# Executive
cd RoboCompAGMExecutive
cmake .
sudo make install

