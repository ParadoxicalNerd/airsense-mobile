#!/usr/bin/env python3
import serial
import requests
import time
import sys
import subprocess
import pycurl
from io import BytesIO
from gps_parsing import GPS_Parser
import Adafruit_DHT as dht
import random
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C
import RPi.GPIO as gpio

url = "https://things-pro.ag.purdue.edu:8080/api/v1/OAsuSaV1G6w6Vu2lv0Fa/telemetry"
prev_hum = 50
prev_temp = 20

reset_pin = None
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
pm = PM25_I2C(i2c, reset_pin)


class FONA_3G:
    def __init__(self, baudrate):
        self.baudrate = baudrate
    
    def reset(self):
        reset_pin = 18
        gpio.setmode(gpio.BCM)
        gpio.setup(reset_pin, gpio.OUT)
        gpio.output(reset_pin, gpio.LOW)
        time.sleep(0.2)
        gpio.output(reset_pin, gpio.HIGH)

    def pass_command(self, string):
        self.ser.write(string + b"\r\n")
        self.ser.flush()

    def read_output(self):
        time.sleep(1)
        line = ""
        while self.ser.inWaiting() > 0:
            line += self.ser.read(1).decode("utf-8")
        # return '\n'.join(line.splitlines()[1:])
        return line

    def print_output(self):
        line = self.read_output()
        print(line)

    def okay(self):
        self.pass_command(b"AT")
        return "OK" in self.read_output()

    def get_coordinates(self):
        self.pass_command(b"AT+CGPSINFO")
        return GPS_Parser(self.read_output())

    def enable_gps(self):
        # No need to use as I have enabled GPS on start
        """False means that gps is already enabled"""
        self.pass_command(b"AT+CGPS=1")
        return self.read_output()

    def disable_gps(self):
        """False means that gps is already disabled"""
        self.pass_command(b"AT+CGPS=0,1")
        return self.read_output()

    # TODO: Error checking does not work for some reason

    # Start PPPD
    def openPPPD(self):
        subprocess.call("sudo pon fona", shell=True)
        print("Turning on cellular")

    # Stop PPPD
    def closePPPD(self):
        subprocess.call("sudo poff fona", shell=True)
        print("Turning off cellular")

    def close_serial(self):
        self.ser.close()

    def open_serial(self):
        try:
            self.ser = serial.Serial("/dev/ttyAMA0", self.baudrate, timeout=1)
        except OSError:
            print(
                "The port seems busy. Are you sure you have not got the port open on another window?"
            )
            exit(-1)


def read_temperature_humidity():
    humidity, temperature = dht.read_retry(dht.DHT22, 21)
    humidity_value = round(humidity, 2)
    temperature_value = round(temperature, 2)

    if temperature_value > (prev_temp + 5):
        temperature_value = prev_temp
    elif temperature_value < (prev_temp - 5):
        temperature_value = prev_temp

    if humidity_value > (prev_hum + 100):
        humidity_value = prev_hum
    elif humidity_value < (prev_hum - 100):
        humidity_value = prev_hum

    return temperature_value, humidity_value


def read_pm():
    aqdata = pm.read()
    return aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"]

cache = []

if __name__ == "__main__":
    fona = FONA_3G(115200)
    fona.openPPPD()
    time.sleep(120)
    while True:
        time.sleep(5)

        try:

            # Get GPS Coordinates
            #fona.open_serial()
            #time.sleep(1)
            #coordinates = fona.get_coordinates()
            #fona.close_serial()

            # Start internet connectivity
            #fona.openPPPD()
            #time.sleep(5)

            # Read DHT22
            temperature, humidity = read_temperature_humidity()

            # Read PM
            pm10, pm25, pm100 = read_pm()

            data = {
                "ts":int(time.time()),
                "lat": "40.42967",
                "long": "-86.91179",
                #"alt": coordinates.altitude,
                #"speed": coordinates.speed,
                #"heading": coordinates.course,
                "temperature": temperature,
                "humidity": humidity,
                "pm10": pm10,
                "pm25": pm25,
                "pm100": pm100
            }

            # Send the data
            res = requests.post(url=url, json=data)
            print(res)


            # print(res)
            # fona.closePPPD()

        except Exception as e:
            print(e)
            # TODO: Implement caching

        finally:
            pass
#        fona.close_serial()

    # print(fona.enable_gps())
    # time.sleep(20)
    # try:
    #    while True:
    #        print(fona.get_coordinates())
    #        time.sleep(5)
    # except Exception:
    #    pass
    # print(fona.disable_gps())

