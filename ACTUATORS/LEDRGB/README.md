The script **ledbar.py** implements the Joystick module from LinkerKit.

More details can be found here: http://www.linkerkit.de/index.php?title=LK-LEDM

'''
sudo apt-get update
sudo apt-get install build-essential python-dev git scons swig
git clone https://github.com/jgarff/rpi_ws281x
cd rpi_ws281x
sudo apt-get install scons
sudo scons
cd python
sudo python ez_setup.py
sudo python setup.py install
cd examples/
'''