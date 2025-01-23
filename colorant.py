import cv2
import numpy as np
import threading
import time

from screen_cap import ScreenCapture
from mouse import ArduinoMouse

class Colorant:
    LOWER_COLOR = np.array([140, 110, 150])
    UPPER_COLOR = np.array([150, 195, 255])
    THRESHOLD = 60

    def __init__(self, x, y, grabzone):
        self.arduinomouse = ArduinoMouse()
        self.grabber = ScreenCapture()
        self.toggled = False
        self.triggertoggled = False
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def toggle(self, type):
        if type == "Triggerbot":
            self.triggertoggled = not self.triggertoggled
        elif type == "Aimbot":
            self.toggled = not self.toggled
        time.sleep(0.2)

    def run(self):
        while True:
            if hasattr(self, 'toggled') and self.toggled:
                self.process("move")
            elif hasattr(self, 'triggertoggled') and self.triggertoggled:
                self.process("click")

    def process(self, action):
        screen = self.grabber.get_screen()
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.LOWER_COLOR, self.UPPER_COLOR)
        dilated = cv2.dilate(mask, None, iterations=5)
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if not contours:
            return

        contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(contour)
        center = (x + w // 2, y + h // 2)

        if action == "move":
            cX = x + w // 2
            cY = y + h // 2
            x_diff = cX - self.grabber.grabzone // 2
            y_diff = cY - self.grabber.grabzone // 2
            self.arduinomouse.move(x_diff * 0.2, y_diff * 0.2)
        elif action == "click" and abs(center[0] - self.grabber.grabzone // 2) <= 4 and abs(center[1] - self.grabber.grabzone // 2) <= 10:
            self.arduinomouse.click()

    def close(self):
        if hasattr(self, 'arduinomouse'):
            self.arduinomouse.close()
        self.toggled = False
        self.triggertoggled = False

    def __del__(self):
        self.close()


    def close(self):
        if hasattr(self, 'arduinomouse'):
            self.arduinomouse.close()
        self.toggled = False
        self.triggertoggled = False

    def __del__(self):
        self.close()
