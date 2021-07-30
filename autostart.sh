#!/bin/sh

# Disables the gui
# sudo init 3

# Resets FONA

#   Exports pin to userspace
#sudo echo "21" > /sys/class/gpio/export

# Sets pin 18 as an output
#sudo echo "out" > /sys/class/gpio/gpio21/direction

# Sets pin 18 to low
#sudo echo "0" > /sys/class/gpio/gpio21/value

#sleep 2

# Sets pin 18 to high
#sudo echo "1" > /sys/class/gpio/gpio21/value

# sleep 5

sudo pon fona
cd "/home/pi/standalone/Revision 2"
echo "Execution started" > logs.txt
python3 main.py > logs.txt & 
