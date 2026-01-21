from ultralytics import YOLO
import cv2
import numpy as np
import hashlib
import time

class PrivacyEngine:
    def __init__(self, model_path):
        print(f"Loading Model from {model_path}...")
        self.model = YOLO(model_path, task="pose")
        self.block_size = 15
        self.pad_ratio = 1.0

    def pixelate(self, image, x1, y1, x2, y2):
        """Helper to pixelate a region"""
        face_roi = image[y1:y2, x1:x2]
        h, w = face_roi.shape[:2]
        if w < 10 or h < 10: return
        
        small = cv2.resize(face_roi, (self.block_size, self.block_size), interpolation=cv2.INTER_LINEAR)
        pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
        image[y1:y2, x1:x2] = pixelated

    def process_frame(self, frame):
        start_time = time.time()
        results = self.model(frame, verbose=False)
        
        for result in results:
            if result.keypoints is None: continue
            
            for person_kps in result.keypoints.xy:
                kps = person_kps.cpu().numpy()
                face_points = kps[:5]
                valid_x = [p[0] for p in face_points if p[0] > 1]
                
                if len(valid_x) >= 3:
                    min_x, max_x = int(min(valid_x)), int(max(valid_x))
                    face_span = max_x - min_x
                    
                    center_x = (min_x + max_x) // 2
                    center_y = int(np.mean([p[1] for p in face_points if p[1] > 1]))

                    center_y -= int(face_span * 0.10)
                    
                    radius_w = int(face_span * 0.6)
                    radius_h = int(face_span * 0.9)

                    h, w = frame.shape[:2]
                    x1 = max(0, center_x - radius_w)
                    y1 = max(0, center_y - radius_h)
                    x2 = min(w, center_x + radius_w)
                    y2 = min(h, center_y + radius_h)

                    self.pixelate(frame, x1, y1, x2, y2)

        latency = (time.time() - start_time) * 1000
        frame_bytes = frame.tobytes()
        integrity_hash = hashlib.sha256(frame_bytes).hexdigest()

        return frame, latency, integrity_hash