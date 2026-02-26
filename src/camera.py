import cv2
import threading
import time
from config.settings import settings

class CameraManager:
    def __init__(self):
        self.cap = cv2.VideoCapture(settings.camera_device)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, settings.resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.resolution[1])
        
        self.latest_frame = None
        self.running = True
        self.lock = threading.Lock()

        self.thread = threading.Thread(target=self._update_camera, daemon=True)
        self.thread.start()
        
        time.sleep(2)

    def _update_camera(self):
        while self.running:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    with self.lock:
                        self.latest_frame = frame
                else:
                    time.sleep(0.1)
            else:
                time.sleep(0.1)

    def get_frame(self):
        with self.lock:
            if self.latest_frame is not None:
                return self.latest_frame.copy()
        return None

    def release(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        self.cap.release()