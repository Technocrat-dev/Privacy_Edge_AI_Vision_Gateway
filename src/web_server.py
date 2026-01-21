from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

camera_ref = None
engine_ref = None

def generate_frames():
    while True:
        if camera_ref is None: break
        
        frame = camera_ref.read()
        if frame is None: continue

        processed_frame, latency, start_hash = engine_ref.process_frame(frame)

        cv2.putText(processed_frame, f"Hash: {start_hash[:8]}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(processed_frame, f"Lat: {latency:.1f}ms", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def start_server(camera, engine):
    global camera_ref, engine_ref
    camera_ref = camera
    engine_ref = engine
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)