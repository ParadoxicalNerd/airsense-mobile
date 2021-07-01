#!/usr/bin/env python3
import serial
import requests
import time
import sys
import subprocess
import pycurl
from io import BytesIO

import random
from OPC_N3 import OPC

url = "https://things-pro.ag.purdue.edu:8080/api/v1/OAsuSaV1G6w6Vu2lv0Fa/telemetry"

if __name__ == "__main__":
    opc = OPC()
    opc.fanOn()
    opc.laserOn()
    
    for i in range(10):
        time.sleep(5)
        try:
            
            histogram = opc.getHist()
            
            temperature, humidity = histogram['OPC-T'], histogram['OPC-RH']
            pm10, pm25, pm100 = histogram['pm1'], histogram['pm2.5'], histogram['pm10']

            data = {
                "ts":int(time.time()),
                "lat": "40.42967",
                "long": "-86.91179",
                "temperature": temperature,
                "humidity": humidity,
                "pm10": pm10,
                "pm25": pm25,
                "pm100": pm100
            }

            # Send the data
            res = requests.post(url=url, json=data)
            print(res)

        except Exception as e:
            print(e)

    opc.laserOff()
    opc.fanOff()
    opc.close()
