import os, threading, time, sys

try:
    import numpy as np
except ImportError:
    os.system("pip install numpy")
    import numpy as np

try:
    import mss
except ImportError:
    os.system("pip install mss")
    import mss

try:
    from PIL import Image
except ImportError:
    os.system("pip install Pillow")
    from PIL import Image

try:
    import msvcrt
except ImportError:
    os.system("pip install msvcrt")
    import msvcrt


try:
    import ndi
except ImportError:
    print("[Error] NDI lib not installed. Follow (https://github.com/buresu/ndi-python) for help")
    exit()

class ScreenCapture:  
    def __init__(self, x=0, y=0, grabzone=500):
        self.x, self.y, self.grabzone = x, y, grabzone
        self.screen = np.zeros((grabzone, grabzone, 3), np.uint8)
        self.pillow = None
        self.lock = threading.Lock()
        self.frame_count = 0
        self.start_time = time.time()
        self.running = True

        # Initialize NDI
        if not ndi.initialize():
            print('[Error] Failed to initialize NDI. Check (https://docs.ndi.video/all/developing-with-ndi/sdk)')
            return

        # Create NDI Finder
        ndi_find = ndi.find_create_v2()
        if ndi_find is None:
            print('[Error] Failed to create NDI finder. Check (https://docs.ndi.video/all/developing-with-ndi/sdk)')
            return

        # Continuously refresh NDI sources until selected
        sources = []
        buffer = ""
        print("Searching for NDI sources... Type a number to select a source.\n")

        try:
            while True:
                ndi.find_wait_for_sources(ndi_find, 100)
                new_sources = ndi.find_get_current_sources(ndi_find)
                
                if new_sources != sources:
                    sources = new_sources
                    # Clear previous output
                    print("\033[H\033[J", end="") 
                    print("Searching for NDI sources... Type a number to select a source.\n")
                    print("Available NDI sources:")
                    if sources:
                        for i, source in enumerate(sources):
                            print(f"{i}. {source.ndi_name}")
                    else:
                        print("No sources found yet.")
                    print(f"\nCurrent input: {buffer}")
                
                # Check for user input
                if msvcrt.kbhit():
                    char = msvcrt.getch().decode('utf-8')
                    
                    if char in ('\b', '\x7f'): 
                        if buffer:
                            buffer = buffer[:-1]
                    elif char in ('\r', '\n'):
                        if buffer:
                            try:
                                selection = int(buffer)
                                if 0 <= selection < len(sources):
                                    selected_source = sources[selection]
                                    print(f"\nSelected source: {selected_source.ndi_name}")
                                    break  
                                else:
                                    print("\nInvalid selection. Please try again.")
                                    buffer = ""
                            except ValueError:
                                print("\nPlease enter a valid number.")
                                buffer = ""

                    elif char.isdigit():
                        buffer += char
                    
                    print(f"\rCurrent input: {buffer}                 ", end="")
                    sys.stdout.flush()
                
                time.sleep(0.1)
                    
        except KeyboardInterrupt:
            print("\nSearch cancelled by user.")

        if not sources:
            print('[Error] No NDI sources found. Ensure there is an NDI broadcast on your network, see (https://github.com/DistroAV/DistroAV)')
            return

        # Create NDI Receiver
        ndi_recv_create = ndi.RecvCreateV3()
        ndi_recv_create.color_format = ndi.RECV_COLOR_FORMAT_BGRX_BGRA
        self.ndi_recv = ndi.recv_create_v3(ndi_recv_create)

        if self.ndi_recv is None:
            print('[Error] Failed to create NDI receiver. Check (https://docs.ndi.video/all/developing-with-ndi/sdk)')
            return

        # Connect to the first available NDI source
        ndi.recv_connect(self.ndi_recv, sources[0])
        ndi.find_destroy(ndi_find)

        # Start Capture Threads
        self.start()

    def start(self):
        threading.Thread(target=self.capture_screen, daemon=True).start()
        threading.Thread(target=self.capture_ndi, daemon=True).start()

    def update(self):
        while True:
            video_frame = ndi.VideoFrameV2()
            metadata = ndi.MetadataFrame()
            package, _ = ndi.recv_capture_v2(self.ndi_recv, video_frame, metadata, None, 5000)  # Timeout: 5 sec

            if package == ndi.FRAME_TYPE_VIDEO:
                with self.lock:
                    # Extract RGB from package
                    self.screen = np.array(video_frame.data)[:, :, :3]  
                    self.pillow = Image.fromarray(self.screen, 'RGB')

                # FPS counter
                self.frame_count += 1
                elapsed_time = time.time() - self.start_time
                if elapsed_time >= 1:
                    fps = self.frame_count / elapsed_time
                    print(f"FPS: {fps:.2f}", end="\r")
                    self.frame_count = 0
                    self.start_time = time.time()

                ndi.recv_free_video_v2(self.ndi_recv, video_frame)

    def get_screen(self):
        with self.lock:
            return self.screen.copy()

    def get_pillow(self):
        with self.lock:
            if self.pillow is None:
                return None
            return Image.frombytes("RGB", self.pillow.size, self.pillow.bgra, "raw", "BGRA")

