"""
Code to use the Alphasense OPC-N3 sensor with the Raspberry Pi

@author Pankaj Meghani
@date 30 July, 2021
"""

# TODO
# Fan is having issue. Check what's up with it

from __future__ import print_function
import serial
import time
import struct
import datetime

integration = 5

# NAMING VARIABLES
OPCNAME = "TestOPC"
OPCPORT = "/dev/ttyACM0"
LOCATION = "Lab2"
wait = 1e-06
debug = False


class OPC:
    def __init__(self, ser):
        self.ser = ser

    # Turn fan

    def fanOff(self):
        T = 0  # Tries counter
        while True:
            ser.write(bytearray([0x61, 0x03]))
            nl = ser.read(2)
            if debug:
                print(nl)
            T = T + 1
            if nl == (b"\xff\xf3" or b"\xf3\xff"):
                time.sleep(wait)
                ser.write(bytearray([0x61, 0x02]))
                nl = ser.read(2)
                if debug:
                    print(nl)
                time.sleep(2)
                return
            elif T > 20:
                time.sleep(3)  # time for spi buffer to reset
                T = 0
            else:
                time.sleep(wait * 10)  # wait 1e-05 before next commnad

    # Turn fan and laser on
    def fanOn(self):
        T = 0  # Tries counter
        while True:
            ser.write(bytearray([0x61, 0x03]))
            nl = ser.read(2)
            if debug:
                print(nl)
            T = T + 1
            if nl == (b"\xff\xf3" or b"xf3\xff"):
                time.sleep(wait)
                ser.write(bytearray([0x61, 0x03]))
                nl = ser.read(2)
                if debug:
                    print(nl)
                time.sleep(2)
                return
            elif T > 20:
                print("Reset SPI")
                time.sleep(3)  # time for spi buffer to reset
                T = 0
            else:
                time.sleep(wait * 10)  # wait 1e-05 before next commnad

    def LaserOn(self):
        T = 0  # Tries counter
        while True:
            ser.write(bytearray([0x61, 0x03]))
            nl = ser.read(2)
            if debug:
                print(nl)

            T = T + 1
            if nl == (b"\xff\xf3" or b"\xf3\xff"):
                time.sleep(wait)
                ser.write(bytearray([0x61, 0x07]))
                nl = ser.read(2)
                if debug:
                    print(nl)
                time.sleep(wait)
                return
            elif T > 20:
                print("Reset SPI")
                time.sleep(3)  # time for spi buffer to reset
                T = 0
            else:
                time.sleep(wait * 10)  # wait 1e-05 before next commnad

    def LaserOff(self):
        print("Lazer Off")

        T = 0  # Tries counter
        while True:
            ser.write(bytearray([0x61, 0x03]))
            nl = ser.read(2)
            if debug:
                print(nl)
            T = T + 1
            if nl == (b"\xff\xf3" or b"\xf3\xff"):
                time.sleep(wait)
                ser.write(bytearray([0x61, 0x06]))
                nl = ser.read(2)
                if debug:
                    print(nl)
                time.sleep(wait)
                return
            elif T > 20:
                print("Reset SPI")
                time.sleep(3)
                T = 0
            else:
                time.sleep(wait * 10)  # wait 1e-05 before next commnad

    def humidity_conversion(self, ans):
        # ans is  combine_bytes(ans[52],ans[53])
        RH = 100 * (ans / (2 ** 16 - 1))
        return RH

    def temperature_conversion(self, ans):
        # ans is  combine_bytes(ans[52],ans[53])
        Temp = -45 + 175 * (ans / (2 ** 16 - 1))
        return Temp

    def combine_bytes(self, LSB, MSB):
        return (MSB << 8) | LSB

    def response_bytes(self, response):
        """
        Get ride of the 0x61 bytes responce from the hist data, returning just the wanted data
        """
        hist_response = []
        # Each of the 86 bytes we expect to be returned is prefixed by 0xFF.
        for j, k in enumerate(response):
            # Throw away 0th, 2nd, 4th, 6th bytes, etc.
            if ((j + 1) % 2) == 0:
                hist_response.append(k)
        return hist_response

    def histogram_parse(self, ans):
        data = {}
        data["Bin 0"] = self.combine_bytes(ans[0], ans[1])
        data["Bin 1"] = self.combine_bytes(ans[2], ans[3])
        data["Bin 2"] = self.combine_bytes(ans[4], ans[5])
        data["Bin 3"] = self.combine_bytes(ans[6], ans[7])
        data["Bin 4"] = self.combine_bytes(ans[8], ans[9])
        data["Bin 5"] = self.combine_bytes(ans[10], ans[11])
        data["Bin 6"] = self.combine_bytes(ans[12], ans[13])
        data["Bin 7"] = self.combine_bytes(ans[14], ans[15])
        data["Bin 8"] = self.combine_bytes(ans[16], ans[17])
        data["Bin 9"] = self.combine_bytes(ans[18], ans[19])
        data["Bin 10"] = self.combine_bytes(ans[20], ans[21])
        data["Bin 11"] = self.combine_bytes(ans[22], ans[23])
        data["Bin 12"] = self.combine_bytes(ans[24], ans[25])
        data["Bin 13"] = self.combine_bytes(ans[26], ans[27])
        data["Bin 14"] = self.combine_bytes(ans[28], ans[29])
        data["Bin 15"] = self.combine_bytes(ans[30], ans[31])
        data["Bin 16"] = self.combine_bytes(ans[32], ans[33])
        data["Bin 17"] = self.combine_bytes(ans[34], ans[35])
        data["Bin 18"] = self.combine_bytes(ans[36], ans[37])
        data["Bin 19"] = self.combine_bytes(ans[38], ans[39])
        data["Bin 20"] = self.combine_bytes(ans[40], ans[41])
        data["Bin 21"] = self.combine_bytes(ans[42], ans[43])
        data["Bin 22"] = self.combine_bytes(ans[44], ans[45])
        data["Bin 23"] = self.combine_bytes(ans[46], ans[47])
        # MTof is in 1/3 us, value of 10=3.33us
        data["MToF"] = struct.unpack("f", bytes(ans[48:52]))[0]
        data["period"] = self.combine_bytes(ans[52], ans[53])
        data["FlowRate"] = self.combine_bytes(ans[54], ans[55])
        data["OPC-T"] = self.temperature_conversion(
            self.combine_bytes(ans[56], ans[57])
        )
        data["OPC-RH"] = self.humidity_conversion(
            self.combine_bytes(ans[58], ans[59]))
        data["pm1"] = struct.unpack("f", bytes(ans[60:64]))[0]
        data["pm2.5"] = struct.unpack("f", bytes(ans[64:68]))[0]
        data["pm10"] = struct.unpack("f", bytes(ans[68:72]))[0]
        data["Check"] = self.combine_bytes(ans[84], ans[85])

        #  print(data)
        return data

    def getHist(self):
        T = 0  # Counter variable
        while True:
            # Initiate tranmission of histogram dataset
            ser.write([0x61, 0x30])
            nl = ser.read(2)

            if debug:
                print(nl)

            T = T + 1

            if nl == (b"\xff\xf3" or b"\xf3\xff"):  # Check if response is valid
                for i in range(86):  # Send 86 bytes
                    ser.write([0x61, 0x01])
                    time.sleep(wait)

                ans = bytearray(ser.readall())
                ans = self.response_bytes(ans)  # Strip the unwanted bytes
                data = self.histogram_parse(ans)
                return data
            elif T > 20:
                #   print("Reset SPI")
                time.sleep(3)
            else:
                time.sleep(wait * 10)  # wait 1e-05 before next commn


if __name__ == "__main__":
    serial_opts = {
        "port": OPCPORT,
        "baudrate": 9600,
        "parity": serial.PARITY_NONE,
        "bytesize": serial.EIGHTBITS,
        "stopbits": serial.STOPBITS_ONE,
        "xonxoff": False,
        "timeout": 1,
    }

    # wait for opc to boot
    time.sleep(2)

    ser = serial.Serial(**serial_opts)

    # start up dance
    print("Init:")
    opc = OPC(ser)
    time.sleep(1)

    print("Fan Off:")
    opc.fanOff()
    opc.LaserOff()
    time.sleep(5)

    print("Fan on:")
    opc.fanOn()
    opc.LaserOn()
    time.sleep(5)

    print(OPCNAME, "Ready")

    # time loop
    for _ in range(3):

        data = opc.getHist()
        ts = time.time()
        tnow = datetime.datetime.fromtimestamp(
            ts).strftime("%Y-%m-%d %H:%M:%S")

        try:
            # print(tnow + "," + str(data['Bin 0']) + "," + str(data['Bin 1']) + "," + str(data['Bin 2']) + "," + str(data['Bin 3']) + "," + str(data['Bin 4']) + "," + str(data['Bin 5']) + "," + str(data['Bin 6']) + "," + str(data['Bin 7']) + "," + str(data['Bin 8']) + "," + str(data['Bin 9']) + "," + str(data['Bin 10']) + "," + str(data['Bin 11']) + "," + str(data['Bin 12']) + "," + str(data['Bin 13']) + "," + str(data['Bin 14']) + "," + str(data['Bin 15']) + "," + str(
            #    data['Bin 16']) + "," + str(data['Bin 17']) + "," + str(data['Bin 18']) + "," + str(data['Bin 19']) + "," + str(data['Bin 20']) + "," + str(data['Bin 21']) + "," + str(data['Bin 22']) + "," + str(data['Bin 23'])+ ","+str(data['period']) + "," + str(data['FlowRate']) + "," + str(data['Temp']) + "," + str(data['RH']) + "," + str(data['pm1']) + "," + str(data['pm2.5']) + "," + str(data['pm10']) + "," + str(data['Check']), file=f)
            print(
                OPCNAME,
                " Time",
                tnow,
                " Temp:",
                str(data["OPC-T"]),
                " RH:",
                str(data["OPC-RH"]),
                " PM1:",
                str(data["pm1"]),
                "PM2.5:",
                str(data["pm2.5"]),
                "PM10:",
                str(data["pm10"]),
            )
        except Exception as e:  # if get gist falues and reurn NoData
            print("Error")
            print(e)

        time.sleep(5)

    print("Closing:")
    opc.fanOff()
    opc.LaserOff()
    ser.close()
