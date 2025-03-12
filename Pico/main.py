import sys, select, struct, machine

"""
This code could vary greatly depending on your mouse and the sensor it uses, 
this code worked for me using the PAW3395 optical gaming sensor and an Attack Shark X3 mouse, 
but will likley be different depending on your mouse hardware.

Would recommend first trying out the triggerbot function before any mouse move as it is much easier
"""

CLICK_PIN = 15  # Mouse click pin (connect to transistor to short mouse click button)
click_pin = machine.Pin(CLICK_PIN, machine.Pin.OUT)
click_pin.value(0)

# SPI configuration pins
SPI_SCK_PIN  = 10
SPI_MISO_PIN = 11
SPI_MOSI_PIN = 12
SPI_CS_PIN   = 13

spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  sck=machine.Pin(SPI_SCK_PIN),
                  mosi=machine.Pin(SPI_MOSI_PIN),
                  miso=machine.Pin(SPI_MISO_PIN))
cs = machine.Pin(SPI_CS_PIN, machine.Pin.OUT)
cs.value(1) 

def send_spi(data):
    cs.value(0)
    spi.write(data)
    cs.value(1)

def read_spi():
    cs.value(0)
    data = spi.read(5)
    cs.value(1)
    return data

# main loop
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)

while True:
    events = poller.poll(10)
    if events:
        cmd = sys.stdin.read(1)
        if cmd:
            if cmd == 'C':  # click
                click_pin.value(1)
            elif cmd == 'U':  # unclick
                click_pin.value(0)
            elif cmd == 'M':  # move
                # Read two additional bytes representing move_x and move_y (signed bytes)
                move_data = sys.stdin.read(2)
                if move_data and len(move_data) == 2:
                    move_x = struct.unpack('b', move_data[0:1])[0]
                    move_y = struct.unpack('b', move_data[1:2])[0]

                    # Read current sensor data
                    sensor_data = read_spi()
                    modified_data = bytearray(sensor_data)

                    # Adjust sensor values by the movement delta
                    modified_data[1] = (modified_data[1] + move_x) & 0xFF
                    modified_data[2] = (modified_data[2] + move_y) & 0xFF

                    # Send modified data
                    send_spi(modified_data)
