import os, threading, time

try:
    import numpy as np
except ImportError:
    os.system("pip install numpy")
    import numpy as np

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
        
        # Select NDI source
        while True:
                print("\nSearching for NDI sources... (3s)")
                ndi.find_wait_for_sources(ndi_find, 3000)
                sources = ndi.find_get_current_sources(ndi_find)

                if sources:
                    print(f"Found {len(sources)} NDI source(s):")
                    for i, src in enumerate(sources):
                        print(f"[{i}] {src.ndi_name}")

                    user_input = input("Enter source number or press enter to restart: ")

                    if user_input.isdigit():
                        index = int(user_input)
                        if 0 <= index < len(sources):
                            source = sources[index] 
                            break 
                        else:
                            print("[Error] Invalid selection. Please enter a valid number.")
                else:
                    choice = input("[Error] No NDI sources found. Press Enter to retry: ")

        # Create NDI Receiver
        ndi_recv_create = ndi.RecvCreateV3()
        ndi_recv_create.color_format = ndi.RECV_COLOR_FORMAT_BGRX_BGRA
        self.ndi_recv = ndi.recv_create_v3(ndi_recv_create)

        if self.ndi_recv is None:
            print('[Error] Failed to create NDI receiver. Check (https://docs.ndi.video/all/developing-with-ndi/sdk)')
            return

        # Connect to the first available NDI source
        ndi.recv_connect(self.ndi_recv, source)
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

