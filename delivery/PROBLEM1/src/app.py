from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from ultralytics import YOLO
import io
from PIL import Image

app = FastAPI()

model_path =""
model = YOLO("")
labels = model.names

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # run model on frame
    results = model(frame, verbose=False)
    detections = results[0].boxes

    detected_items = []
    for det in detections:
        xyxy = det.xyxy.cpu().numpy().squeeze().tolist()
        cls = int(det.cls.item())
        conf = det.conf.item()
        detected_items.append({
            "class": labels[cls],
            "confidence": conf,
            "bbox": xyxy,
        })

    return JSONResponse(content={"detections": detected_items})
