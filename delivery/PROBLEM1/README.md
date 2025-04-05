## Overview
This project aims to develop a computer vision model capable of accurately classifying grocery products based on images.

## How to run PROBLEM1 (kind of solved)

Go to terminal and use the following command:

```
cd delivery/PROBLEM1
```

And then run:
```
python main.py --val_dir ../val_dir
python main.py --val_dir ../val_dir

```
One example could be:
```
python main.py --val_dir ../bilder
```
## Problem 2 is not solved, but... 
there is a cool frontend solution where you can take pictures with "analyze frame", and then you would get printed out identified item in the conosle


## Rest is just general information about repository
### Approach
Model Choice:
We use Ultralytics YOLO (v11n) for object detection. The model is fine-tuned (or used directly) to distinguish between 26 different product categories. We leverage a pretrained YOLO model from the Ultralytics hub and fine-tune it with our dataset.

## Data Preprocessing & Augmentation:

Data Structure: The dataset is organized into folders, each named after the product's PLU/GTIN code. 
Each folder contains images, JSON annotations, and visualization files.

### Preprocessing:

We restructure the dataset into a global format with separate train and validation folders for images and labels.

We convert annotation files from JSON to YOLO format, where each line contains:
class_id x_center y_center width height

### Inference Pipeline:
The detection pipeline is implemented in a Python script that loads the YOLO model, processes video or image inputs, 
and outputs detection results. A simple frontend in React opens the camera, captures a frame, and sends it to a backend 
API that runs the model and returns predictions.

### Cloud Training:
For scalability and faster training, we used Google colab to train the model using T4 GPU


## Setup and Running the Code


GPU with CUDA (for training/inference)

Node.js (for frontend)

Virtual environment (recommended)

#### Backend Setup (YOLO Training & Inference)

Create and Activate a Virtual Environment:
```bash
cd PROBLEM1
python -m venv .venv
source .venv/bin/activate  # or use .venv\Scripts\activate on Windows

```

Install Dependencies:
```bash
pip install -r requirements.txt

```bash
Running code
```
python main.py <args>
```

Inference / Detection:

To run the detection script (e.g., on a video file or webcam), use:
```bash
python detect.py --model path/to/best.pt --source 0 --thresh 0.5 --resolution 640x480

```
For a USB camera, use --source usb0 (or appropriate index).

#### Frontend Setup (React Camera Analyzer)
Make sure that pnpm and node v20 is installed

Navigate to the Frontend Folder:
```bash
cd frontend

```
Install Dependencies:

```
pnpm i
```

Run the Development Server:
```
pnpm run dev
```

The React app includes a CameraAnalyzer component that:

Opens the camera.

Captures a frame.

Sends it to a backend API for detection.

Displays the detected grocery item.

## Model Architecture & Pretrained Models
Model: YOLO v11n (Ultralytics)

Parameters: ~2.6M parameters with a GFLOP count of 6.5.

Pretrained Weights: We use pretrained weights from the Ultralytics hub (model URL provided in our scripts) and fine-tune them on our grocery dataset.

Data Preprocessing & Augmentation Techniques
Restructuring: The dataset is reorganized into a global format with a clear separation between training and validation data.

Annotation Conversion: JSON annotations are converted to YOLO format using custom scripts.

Augmentation: Although not detailed in this README, common techniques (e.g., random rotations, flips, brightness adjustments) can be added in the data loader pipeline to improve model robustness.

Known Limitations & Areas for Improvement
GPU Memory Constraints: Training with larger batch sizes can lead to CUDA out-of-memory errors. Mixed precision training or gradient accumulation can mitigate this.

Annotation Consistency: Some annotation files may have inconsistent formatting. Future work includes robust error handling and validation of annotation files.

Real-time Performance: Further optimization may be necessary for real-time inference on edge devices.

Scalability: While the current approach works well for a hackathon prototype, scaling up for production will require a more robust deployment strategy (e.g., containerization, cloud-based inference APIs).