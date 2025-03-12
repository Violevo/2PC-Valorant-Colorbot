import time, os, threading
from screen_capture import ScreenCapture
from mouse import PicoMouse

try:
    import win32api  
except ImportError:
    os.system("pip install pywin32")  
    import win32api
try:
    import cv2  
except ImportError:
    os.system("pip install opencv-python") 
    import cv2
try:
    import numpy  
except ImportError:
    os.system("pip install numpy") 
    import numpy

class Colorbot:
    def __init__(self, x, y, grabzone, LOWER_COLOR, UPPER_COLOR):
        self.LOWER_COLOR = LOWER_COLOR  
        self.UPPER_COLOR = UPPER_COLOR  
        self.arduinomouse = PicoMouse()  
        self.grabber = ScreenCapture(x, y, grabzone)  
        threading.Thread(target=self.run, daemon=True).start()
        self.toggled = False 

    def toggle(self):
        self.toggled = not self.toggled 
        time.sleep(0.2) 

    # Threaded keychecker
    def run(self):
        while True:
            if win32api.GetAsyncKeyState(0x02) < 0 and self.toggled:  # right click
                self.process("move") 
            elif win32api.GetAsyncKeyState(0x12) < 0 and self.toggled:  # alt
                self.process("click") 

    def process(self, action):
        screen = self.grabber.get_screen()  
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)  
        mask = cv2.inRange(hsv, self.LOWER_COLOR, self.UPPER_COLOR) 
        dilated = cv2.dilate(mask, None, iterations=5)  #
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if not contours: # no enemies
            return

        # Find the topmost outline (head)
        contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(contour)  
        center = (x + w // 2, y + h // 2)  

        if action == "move":
            # Calculate differences for mouse movement based on contour center
            cX = x + w // 2
            cY = y + 9  
            x_diff = cX - self.grabber.grabzone // 2 
            y_diff = cY - self.grabber.grabzone // 2 
            self.arduinomouse.move(x_diff * 0.2, y_diff * 0.2)  # Move mouse with scaling

        elif action == "click" and abs(center[0] - self.grabber.grabzone // 2) <= 4 and abs(center[1] - self.grabber.grabzone // 2) <= 10:
            # Click the mouse if the target is in the center of the capture zone
            self.arduinomouse.click()

    def close(self):
        if hasattr(self, 'arduinomouse'):
            self.arduinomouse.close()  
        self.toggled = False 

    def __del__(self):
        self.close()
