from ultralytics import YOLO

# Load a COCO-pretrained YOLO11n model
model = YOLO("yolo11n.pt")

results = model.train(data="../../../data.yaml", epochs=10, imgsz=3801)
