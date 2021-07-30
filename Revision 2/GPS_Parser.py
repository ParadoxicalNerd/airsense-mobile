import re
import json

"""
Code to parse the gps data returned by Fona module

@author Pankaj Meghnai 
@date 30 July, 2021
"""

class GPS_Parser:
    def __init__(self, string):
        regex_exp = r"CGPSINFO:([\d.]*)(?:,?)([NS]?)(?:,?)([\d.]*),([EW]?),\d*,[\d.]*,([\d.]*),([\d.]*),(\d*)"

        matches = re.search(regex_exp, string)
        is_okay = re.search(r'\b(OK)\b', string)

        seperator = '.'

        if (is_okay == None):
            okay = False
            latitude = longitude = altitude = speed = course = None
        else:
            okay = True

            latitude = matches.group(1)
            latitude = latitude[:2]+seperator+latitude[2:4]+latitude[5:]
            if (matches.group(2) == 'S'):
                latitude = '-'+latitude

            longitude = matches.group(3)
            longitude = longitude[:3]+seperator+longitude[3:5]+longitude[6:]
            if (matches.group(4)=='W'):
                longitude = '-'+longitude

            altitude = matches.group(5)
            speed = matches.group(6)
            course = matches.group(7)

        self.okay = okay
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.speed = speed
        self.course = course

    def __str__(self):
        return ' '.join([
            str(self.okay),
            self.latitude,
            self.longitude,
            self.altitude,
            self.speed,
            self.course
        ])

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

