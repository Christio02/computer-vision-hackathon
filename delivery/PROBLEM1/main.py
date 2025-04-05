import argparse
from pathlib import Path
from ultralytics import YOLO
from collections import Counter

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--val_dir', type=str, required=True, help='Path to validation image folder')
    parser.add_argument('--model_path', type=str, default='model/best.pt', help='(Optional) Path to YOLO .pt model')
    return parser.parse_args()

def load_model(model_path):
    print(f"[INFO] Loading model from: {model_path}")
    return YOLO(model_path)

def run_inference(model, image_folder):
    image_folder = Path(image_folder)
    image_paths = list(image_folder.glob("*.jpg")) + list(image_folder.glob("*.png"))

    detections = []

    for img_path in image_paths:
        print(f"[INFO] Running detection on: {img_path.name}")
        results = model(img_path)
        names = results[0].names
        for box in results[0].boxes:
            cls = int(box.cls.item())
            detections.append(names[cls])

    return Counter(detections)

def main(opt):
    model = load_model(opt.model_path)
    counts = run_inference(model, opt.val_dir)

    print("\n--- Receipt (Detected Items) ---")
    for item, qty in counts.items():
        print(f"{item}: {qty}")
    print("------------------------------")

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
