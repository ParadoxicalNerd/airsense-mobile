#!/bin/sh
cd /home/pi/standalone
echo "THis has started" > logs.txt
python3 main.py #> logs.txt &


