import os, time
from colorbot import Colorbot

try:
    import keyboard
except ImportError:
    os.system("pip install keyboard")
    import keyboard

try:
    import json
except ImportError:
    os.system("pip install json")
    import json

def main():
    os.system('title Colorbot')

    # Load config
    with open('data.json', 'r') as file:
        config = json.load(file)

    # Update variables
    TOGGLE_KEY = config['TOGGLE_KEY']
    FOV = config['FOV']
    LOWER_COLOR = config['LOWER_COLOR']
    UPPER_COLOR = config['UPPER_COLOR']
    RESOLUTION = config['RESOLUTION']
    CENTER_X, CENTER_Y = RESOLUTION[0] // 2, RESOLUTION[1] // 2
    status = 'Disabled' 

    app = Colorbot(CENTER_X - FOV // 2, CENTER_Y - FOV // 2, FOV, LOWER_COLOR, UPPER_COLOR)
    
    # Toggle loop
    try:
        while True:
            if keyboard.is_pressed(TOGGLE_KEY):
                Colorbot.toggle()
                if Colorbot.toggled:
                    status = 'Enabled'
                else:
                    status = 'Disabled'
            print(f'\r[Status] {status}', end='')
            time.sleep(0.01)
    except (KeyboardInterrupt, SystemExit):
        print('\n[Info] Exiting...\n')
    finally:
        Colorbot.close()

if __name__ == '__main__':
    main()