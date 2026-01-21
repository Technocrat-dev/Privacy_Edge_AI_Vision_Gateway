import cv2
import threading
import time

class VideoStream:
    def __init__(self, source=0):
        self.stream = cv2.VideoCapture(source)
        
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.running = False
        self.lock = threading.Lock()
        self.frame = None

        if not self.stream.isOpened():
            raise ValueError("Could not open camera.")

    def start(self):
        if self.running: return
        self.running = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def update(self):
        while self.running:
            success, frame = self.stream.read()
            if success:
                with self.lock:
                    self.frame = frame
            else:
                self.running = False

    def read(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.running = False
        self.thread.join()
        self.stream.release()