# 2PC Valorant Colorbot

## Fully External & Undetectable 2-Computer Colorbot for Valorant

This project creates an external **colorbot** for **Valorant** that uses a two-computer setup to detect enemy players and trigger mouse movements and clicks, using NDI to transfer video frames between computers. By analysing frames captured by OBS and processing them on a second computer, this simulates mouse movement and clicks in response to the game’s environment, using a Raspberry Pi Pico to interface with the mouse on a hardware level, making it **completely** undetectable to **any** anticheat (tested undetected for VGK).

Aimbot

https://github.com/user-attachments/assets/ac019950-a0ac-433c-b8cd-d820d9b15f62


---

## How Does It Work?

1. **OBS Captures the Valorant Game Window**:
   - OBS is captures the Valorant.exe window as a video stream
2. **The Video Stream Is Sent Over Your Local Network Using OBS-NDI**:
   - OBS streams the captured video to a second computer via the **OBS-NDI** plugin.
3. **The Second Computer Receives This Video Stream Using Python-NDI**:
   - Python-NDI receives the video stream and processes it.
4. **The Program Generates a Similarity Map**:
   - The program compares the pixels of each frame against a colour range of enemy outlines to create a similarity map. In short, this is an image of where the enemy's are in game.
5. **Triggerbot**:

   - If the crosshair has pixels from the similarity map both above and below it (+/- a few horizontal pixels), indicating it's over a player, the program triggers a click function to shoot.

6. **Aimbot Functionality**:

   - For the aimbot, the topmost pixel in the similarity map is subtracted from the crosshair’s position to create a vector (in pixels) pointing to the player’s head.
   - The amount the mouse should move for each pixel is calculated from the following formula:

     $$ 1.07437623 \times \text{Sensitivity}^{-0.9936827126} $$

7. **Triggerbot / Aimbot Data Is Transmitted Over USB**:
   - The processed data (mouse movement and triggerbot signal) is sent over USB to a **Raspberry Pi Pico**.
8. **The Pico Relays Signals to the Mouse Circuit Board**:
   - The Pico decodes the data and relays it through **SPI** to the mouse’s PCB, adding the received movement to the sensor data and simulating mouse movement.
   - When the triggerbot signal is received, the Pico outputs a voltage to simulate a mouse click.

![image](https://github.com/user-attachments/assets/3bc80cc7-9d33-45fb-a8aa-60e86ab7a49a)


---

## Installation

### Hardware Requirements

- **Main Computer**: Capable of running both **Valorant** and **OBS** simultaneously.
- **Second (Less Capable) Computer**: A Raspberry Pi or similar device for processing the NDI stream.
- **Programmable Microcontroller**: A **Raspberry Pi Pico** or any other microcontroller with USB connectivity for communication with the second PC.
- **Ethernet Connection**: A wired Ethernet connection between the main PC and the second PC for low latency.
- **Soldering Kit & Thin Copper Wire**: Required for interfacing the Raspberry Pi Pico with the mouse PCB via SPI and controlling mouse buttons.

---

### Software Requirements

1. **NDI SDK**:

   - Install the NDI SDK for your coding language (Python) and operating system (Windows).
   - Python-NDI can be installed [here](https://github.com/buresu/ndi-python)

2. **OBS-NDI Plugin**:
   - Download and install the **OBS-NDI** plugin on your main computer from [here](https://github.com/DistroAV/DistroAV).
3. **Python Dependencies**:

   - Install the necessary Python libraries:
     ```bash
     pip install numpy opencv-python pyserial termcolor
     ```

4. **Raspberry Pi Pico**:
   - Flash the **MicroPython** firmware onto your Raspberry Pi Pico.
   - Install any necessary libraries for SPI and USB communication (such as `machine`, `time`, and `usb_cdc`).

---

## Setup Instructions

1. **Configure OBS**:
   - Set up OBS to capture the Valorant game window and use the **OBS-NDI** plugin to stream it over the network.
2. **Set Up the Second Computer**:
   - Install Python and the **Python-NDI** library to receive the NDI stream.
   - install the `main.py` file and dependency's to the 2nd computer
3. **Prepare the Raspberry Pi Pico**:
   - Flash MicroPython onto the Raspberry Pi Pico.
   - Upload the Python script to the Pico to decode the triggerbot/aimbot data and relay mouse signals over SPI to the mouse PCB.
4. **Connect the Pico to the Mouse**:
   - Solder the Pico's SPI pins to the mouse's sensor and PCB, ensuring proper connections for mouse movement and button control.
5. **Run the Program**:
   - On the second computer, start the Python program to process the video stream.
   - The Pico should relay the mouse movement and simulate clicks when the triggerbot is triggered.

---

## Credits

- [Initial Development Ideas](https://www.unknowncheats.me/forum/valorant/576868-simple-colorbot-2023-a.html)
- [Colour Filtering](https://www.unknowncheats.me/forum/valorant/587689-fast-hue-l2-distance-based-color-filtering-using-numpy.html)
- [Colour Filtering](https://www.unknowncheats.me/forum/valorant/587689-fast-hue-l2-distance-based-color-filtering-using-numpy.html)
- [Triggerbot Optimisations](https://www.unknowncheats.me/forum/3072055-post10.html)
- [Sensitivity Calculation](https://www.unknowncheats.me/forum/valorant/499748-pixel-silent-aim.html)

---

## Final Notes

This project is **not** a plug-and-play solution and will require some tinkering depending on your hardware, software configuration, and use case. This README outlines the process I personally followed; however, adjustments will likely be necessary for different setups.

---

<p align="center">Educational Purposes Only 📚</p>
