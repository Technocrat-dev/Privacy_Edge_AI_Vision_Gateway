# Secure Edge-Vision Gateway

![Status](https://img.shields.io/badge/Status-Live-success)
![Tech](https://img.shields.io/badge/Stack-YOLOv11%20|%20OpenVINO%20|%20Flask-blue)
![Performance](https://img.shields.io/badge/Latency-9.6ms%20(INT8)-yellow)

**A real-time, privacy-preserving video surveillance pipeline designed for Edge Computing.**

This project acts as a middleware "Gateway" that processes raw video streams locally. It uses **Pose Estimation** to detect humans and dynamically redact PII (faces) before the data ever leaves the device. It ensures **GDPR/APPI compliance** for retail analytics and smart city sensors.

---

## Key Engineering Features

### 1. **Privacy by Design**
Unlike standard face detection (which often fails on side profiles), this system uses **YOLOv11-Pose** to track the human skeleton. It calculates the head position based on shoulder and ear keypoints, creating a robust "Privacy Mask" even when the face is partially obscured.

### 2. **Hardware Optimization**
Optimized using the OpenVINO toolkit.
- **Standard YOLOv11n:** ~41ms latency (24 FPS)
- **OpenVINO Optimized:** ~9.6ms latency (49+ FPS)
- **Result:** **4.2x Speedup**

### 3. **Chain of Custody (SHA-256 Hashing)**
Every processed frame is cryptographically signed in real-time. A rolling **SHA-256 hash** is displayed on the dashboard, ensuring the video stream has not been tampered with (Deepfake/Edit protection).

### 4. **Asynchronous Architecture**
Implements a **Producer-Consumer Threading Model**:
- **Thread A:** Captures Hardware I/O (Camera) at max polling rate.
- **Thread B:** Runs AI Inference (CPU-Bound).
- **Result:** Decouples inference lag from video playback, preventing "stuttering."

---

## Tech Stack
- **AI Core:** Ultralytics YOLOv11 (Pose Estimation)
- **Inference Engine:** Intel OpenVINO (FP16/INT8 Quantization)
- **Backend:** Python, Flask (Streaming Server)
- **Computer Vision:** OpenCV (Threading, Image Processing)
