import serial
import serial.tools.list_ports
import time
import sys
from termcolor import colored

class ArduinoMouse:
    def __init__(self):
        self.serial_port = serial.Serial()
        self.serial_port.baudrate = 115200
        self.serial_port.timeout = 1
        self.serial_port.port = self.find_serial_port()
        try:
            self.serial_port.open()
        except serial.SerialException:
            print(colored('[Error]', 'red'), colored('Serial port is already being used by another app.', 'white'))
            time.sleep(2)
            sys.exit()

    def find_serial_port(self):
        port = next((port for port in serial.tools.list_ports.comports() if "Pico" in port.description), None)
        if port is not None:
            return port.device
        else:
            print(colored('[Error]', 'red'), colored('No serial port found, check your device and try again.', 'white'))
            time.sleep(2)
            sys.exit()

    def move(self, x, y):
        x = x + 256 if x < 0 else x
        y = y + 256 if y < 0 else y
        self.serial_port.write(b"M" + bytes([int(x), int(y)]))
        
    def click(self):
        self.serial_port.write(b"C")
        time.sleep(0.01)
        self.serial_port.write(b"U")

    def close(self):
        self.serial_port.close()

    def __del__(self):
        self.close()
