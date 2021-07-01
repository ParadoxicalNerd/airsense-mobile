from GPS_Parser import GPS_Parser

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
