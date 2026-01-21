from ultralytics import YOLO

model = YOLO("yolo11n-pose.pt")

print("Exporting model to OpenVINO...")
model.export(format="openvino", half=True)