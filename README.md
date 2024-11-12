# Vehicle Counting with YOLOv5

This project provides an automated solution for vehicle counting using YOLOv5 object detection, applied to traffic monitoring scenarios. By detecting and counting various vehicle classes, such as cars, motorbikes, trucks, and buses, this system supports data-driven decision-making for traffic management and urban planning.

## Project Overview

Our solution leverages CCTV feeds from public traffic cameras in Ho Chi Minh City, accessible through [Ho Chi Minh City Traffic Map](http://giaothong.hochiminhcity.gov.vn/Map.aspx). By analyzing these video streams, the system identifies and counts vehicles passing through different locations, delivering valuable traffic insights to aid congestion management and enhance urban mobility strategies.

### Key Features

- **Vehicle Detection and Counting**: The system detects and counts vehicles from CCTV footage.
- **Multi-Class Detection**: Supports various vehicle types, including cars, motorbikes, trucks, and buses.
- **Customizable Confidence and IoU Thresholds**: Allows fine-tuning detection accuracy based on specific needs.
- **Scalable and Flexible**: Can be deployed on edge devices and scaled for multiple camera feeds.

---

## Setup and Installation

1. Clone this repository.
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt

---

## Model Configuration and Usage
### 1.Training the model
To train the YOLOv5 model, use the following command:
python train.py --data ".../Vehicle_Counting/projectTraffic-main/data/????/data.yaml" --weights yolov5s.pt  --img 640 --batch-size 16 --epochs 50 --device 0

**Note: The trained model will be saved in the directory runs/train/exp?/weights/best.pt.

### 2.Validating the Model
After training, validate the model using the command below:
python val.py --data ".../Vehicle_Counting/projectTraffic-main/data/your_dataset/data.yaml" --weights path/to/best.pt --img 640 --batch-size 16 --device 0

### 3.Capturing Data for Detection
To capture data for detection, execute the trafficCapture.py script:
python modules/trafficCapture.py
Note: remember to change k (filepath) in def capture()

### 4.Running Detection with the Trained Model
To perform object detection with the trained model, use the following command:
python detect_test.py --weights "path/to/best.pt" --source ".../data/images/..." --img 640 --conf-thres 0.25 --device 0 --save-txt --save-conf

### Output directory
All outputs, including model weights, detection results, and label files, are saved in the /runs directory.

