import sys, time, os

try:
    import serial  
except ImportError:
    os.system("pip install pyserial") 
    import serial

import serial.tools.list_ports  

class PicoMouse:
    def __init__(self):
        self.serial_port = serial.Serial()  
        self.serial_port.baudrate = 115200  
        self.serial_port.timeout = 1  
        self.serial_port.port = self.find_serial_port()  
        try:
            self.serial_port.open()  
        except serial.SerialException:
            print("[Error] Serial port is already being used, perhaps the app is already running")
            sys.exit()  

    def find_serial_port(self):
        # Search for a serial port that contains "Pico"
        port = next((port for port in serial.tools.list_ports.comports() if "Pico" in port.description), None)
        if port is not None:
            return port.device 
        else:
            print("[Error] No Pico serial port found, check your device and try again.")
            sys.exit()

    def move(self, x, y):
        # x and y cant be negative
        x = x + 256 if x < 0 else x
        y = y + 256 if y < 0 else y

        # Send to pico
        self.serial_port.write(b"M" + bytes([int(x), int(y)]))

    def click(self):
        self.serial_port.write(b"C")
        time.sleep(0.01)  
        self.serial_port.write(b"U")  

    def close(self):
        self.serial_port.close()
        
    def __del__(self):
        self.close()
