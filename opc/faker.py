import requests
import time
import sys
import json
import random

url = "https://things-pro.ag.purdue.edu:8080/api/v1/sRj9azJtadlvMrXG6fJf/telemetry"

if __name__ == "__main__":
    while True:
        data = {
            "lat": random.uniform(-90, 90),
            "long": random.uniform(-180, 180),
            "temperature": random.uniform(20, 40),
            "humidity":random.uniform(0, 100),
            "pm25":random.uniform(20, 80)
            }
        res = requests.post(url=url, json=data)
        print(res)
        
        time.sleep(5)