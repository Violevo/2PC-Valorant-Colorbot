import numpy as np
import threading
import NDIlib as ndi
import time
import sys
from termcolor import colored

class ScreenCapture:
    def __init__(self):
        if not ndi.initialize():
            print(colored('[Error]', 'red'), colored('failed to initialise NDI.', 'white'))
            time.sleep(2)
            sys.exit()

        ndi_find = ndi.find_create_v2()
        if ndi_find is None:
            print(colored('[Error]', 'red'), colored('No NDI sources found.', 'white'))
            time.sleep(2)
            sys.exit()

        sources = []
        while not sources:
            ndi.find_wait_for_sources(ndi_find, 1000)
            sources = ndi.find_get_current_sources(ndi_find)

        ndi_recv_create = ndi.RecvCreateV3()
        ndi_recv_create.color_format = ndi.RECV_COLOR_FORMAT_BGRX_BGRA
        self.ndi_recv = ndi.recv_create_v3(ndi_recv_create)

        if self.ndi_recv is None:
            print(colored('[Error]', 'red'), colored('Failed to create NDI receiver.', 'white'))
            time.sleep(2)
            sys.exit()

        ndi.recv_connect(self.ndi_recv, sources[0])
        ndi.find_destroy(ndi_find)

    def start(self):
        thread = threading.Thread(target=self.update, daemon=True)
        thread.start()

    def update(self):
        while True:
            t, v = ndi.recv_capture_v2(self.ndi_recv, 5000)
            if t == ndi.FRAME_TYPE_VIDEO:
                self.screen = np.frombuffer(v.data, dtype=np.uint8).reshape(v.yres, v.xres, 4)
                self.frame_count += 1
                elapsed_time = time.time() - self.start_time
                if elapsed_time >= 1:
                    fps = self.frame_count / elapsed_time
                    print(f" FPS: {fps:.2f}", end="\r")
                    self.frame_count = 0
                    self.start_time = time.time()

                ndi.recv_free_video_v2(self.ndi_recv, v)

    def get_screen(self):
        with self.lock:
            return self.screen

    def close(self):
        if hasattr(self, 'ndi_recv') and self.ndi_recv:
            ndi.recv_destroy(self.ndi_recv)
        ndi.destroy()
        if hasattr(self, 'pi') and self.pi.connected:
            self.pi.stop()
        exit()

