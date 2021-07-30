#!/usr/bin/env python3
import serial
import requests
import time
import sys
import subprocess
import pycurl
from io import BytesIO
import csv
import os
import random
from OPC_N3 import OPC

url = "https://things-pro.ag.purdue.edu:8080/api/v1/HkCxa8c0JFdVqVpoGNpX/telemetry"

if __name__ == "__main__":
    opc = OPC()
    opc.fanOn()
    opc.laserOn()

    i = 0

    with open("data.csv", "a", newline="") as f:
        fieldnames = [
            "ts",
            "lat",
            "long",
            "temperature",
            "humidity",
            "pm10",
            "pm25",
            "pm100",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if(os.stat("data.csv").st_size==0):
            writer.writeheader()

        while True:
            try:
                time.sleep(5)
                histogram = opc.getHist()

                temperature, humidity = histogram["OPC-T"], histogram["OPC-RH"]
                pm10, pm25, pm100 = (
                    histogram["pm1"],
                    histogram["pm2.5"],
                    histogram["pm10"],
                )

                data = {
                    "ts": int(time.time()),
                    "lat": "40.429978",
                    "long": "-86.914759",
                    "temperature": temperature,
                    "humidity": humidity,
                    "pm10": pm10,
                    "pm25": pm25,
                    "pm100": pm100,
                }

                writer.writerow(data)
                i+=1

                if i == 6:
                    # Send the data
                    i=0
                    res = requests.post(url=url, json=data)
                    print(res)

            except KeyboardInterrupt as e:
                opc.laserOff()
                opc.fanOff()
                opc.close()
                break

            except Exception as e:
                print(e)
