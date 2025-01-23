import machine
import time
import struct
import ubinascii
from machine import Pin, SPI
from serial import UART

SPI_SCK_PIN = 14
SPI_MISO_PIN = 12
SPI_MOSI_PIN = 13
SPI_CS_PIN = 15
BUTTON_PIN = 16

spi = SPI(0, baudrate=1000000, polarity=0, phase=0, sck=Pin(SPI_SCK_PIN), mosi=Pin(SPI_MOSI_PIN), miso=Pin(SPI_MISO_PIN))
cs = Pin(SPI_CS_PIN, Pin.OUT)
cs.value(1)

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

button = Pin(BUTTON_PIN, Pin.OUT)
button.value(0)

move_x = 0
move_y = 0

def send_spi(data):
    cs.value(0)
    spi.write(data)
    cs.value(1)

def read_spi():
    cs.value(0)
    data = spi.read(5)
    cs.value(1)
    return data

def handle_move():
    global move_x, move_y
    if move_x != 0 or move_y != 0:
        sensor_data = read_spi()
        modified_data = bytearray(sensor_data)
        modified_data[1] += move_x
        modified_data[2] += move_y
        send_spi(modified_data)
        move_x = 0
        move_y = 0

def handle_click():
    button.value(1)
    time.sleep(2)
    button.value(0)

def main():
    while True:
        if uart.any():
            data = uart.read(1)
            if data == b'M':
                move_data = uart.read(2)
                if move_data:
                    move_x, move_y = struct.unpack('bb', move_data)
            elif data == b'C':
                handle_click()
        if move_x == 0 and move_y == 0:
            sensor_data = read_spi()
            send_spi(sensor_data)
        handle_move()

main()
