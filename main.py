import os
import time
import keyboard
from termcolor import colored

# Constants
FOV = 50
CENTER_X, CENTER_Y = 1920 // 2, 1080 // 2

# Placeholder for the Colorant class
class Colorant:
    def __init__(self, x, y, fov):
        self.toggled = False

    def toggle(self, feature_name):
        self.toggled = not self.toggled

    def close(self):
        print("Closing Colorant.")

def print_banner(color, color_color, aimbot_status, aimbot_status_color, triggerbot_status, triggerbot_status_color):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colored('''  
                 ▌ ▐·▪        ▄▄▌  ▄▄▄ . ▌ ▐·      .▄▄ ·      ▄▄·       ▄▄▌        ▄▄▄  ▄▄▄▄·      ▄▄▄▄▄
                ▪█·█▌██ ▪     ██•  ▀▄.▀·▪█·█▌▪     ▐█ ▀.     ▐█ ▌▪▪     ██•  ▪     ▀▄ █·▐█ ▀█▪▪    •██  
                ▐█▐█•▐█· ▄█▀▄ ██▪  ▐▀▀▪▄▐█▐█• ▄█▀▄ ▄▀▀▀█▄    ██ ▄▄ ▄█▀▄ ██▪   ▄█▀▄ ▐▀▀▄ ▐█▀▀█▄ ▄█▀▄ ▐█.▪
                 ███ ▐█▌▐█▌.▐▌▐█▌▐▌▐█▄▄▌ ███ ▐█▌.▐▌▐█▄▪▐█    ▐███▌▐█▌.▐▌▐█▌▐▌▐█▌.▐▌▐█•█▌██▄▪▐█▐█▌.▐▌▐█▌·
                . ▀  ▀▀▀ ▀█▄▀▪.▀▀▀  ▀▀▀ . ▀   ▀█▄▀▪ ▀▀▀▀     ·▀▀▀  ▀█▄▀▪.▀▀▀  ▀█▄▀▪.▀  ▀·▀▀▀▀  ▀█▄▀▪▀▀▀ 
      
                                    Color Aimbot & Triggerbot - developed by violevo\n''', 'red'))
    print(colored('                                          [1]', 'green'), colored('Set aimbot status to', 'white'), colored(aimbot_status, aimbot_status_color))
    print(colored('                                        [2]', 'green'), colored('Set triggerbot status to', 'white'), colored(triggerbot_status, triggerbot_status_color))

def main():
    # Initialize variables
    color = "Purple"
    color_color = "magenta"
    aimbot_status = "Disabled"
    triggerbot_status = "Disabled"
    aimbot_status_color = "red"
    triggerbot_status_color = "red"

    os.system('title Colorant')
    colorant = Colorant(CENTER_X - FOV // 2, CENTER_Y - FOV // 2, FOV)

    print_banner(color, color_color, aimbot_status, aimbot_status_color, triggerbot_status, triggerbot_status_color)

    try:
        while True:
            key_pressed = False

            if keyboard.is_pressed("1"):
                colorant.toggle("Aimbot")
                aimbot_status = "Enabled" if colorant.toggled else "Disabled"
                aimbot_status_color = "green" if colorant.toggled else "red"
                key_pressed = True

            if keyboard.is_pressed("2"):
                colorant.toggle("Triggerbot")
                triggerbot_status = "Enabled" if colorant.toggled else "Disabled"
                triggerbot_status_color = "green" if colorant.toggled else "red"
                key_pressed = True

            if key_pressed:
                print_banner(color, color_color, aimbot_status, aimbot_status_color, triggerbot_status, triggerbot_status_color)
                time.sleep(0.2)  # Prevent multiple triggers for one press

    except (KeyboardInterrupt, SystemExit):
        if 'colorant' in locals():
            colorant.close()

if __name__ == '__main__':
    main()
