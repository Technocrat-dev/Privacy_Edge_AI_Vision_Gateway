from src.camera import VideoStream
from src.inference import PrivacyEngine
from src.web_server import start_server
import time

MODEL_PATH = "models/yolo11n-pose_openvino_model/"

def main():
    print("--- STARTING EDGE GATEWAY ---")
    
    print("[1/3] Warming up camera...")
    cam = VideoStream(source=0).start()
    time.sleep(2.0)

    print("[2/3] Loading OpenVINO Engine...")
    engine = PrivacyEngine(MODEL_PATH)

    print("[3/3] Starting Web Interface on http://localhost:5000")
    try:
        start_server(cam, engine)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        cam.stop()

if __name__ == "__main__":
    main()