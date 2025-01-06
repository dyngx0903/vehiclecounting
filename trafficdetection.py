import os
import cv2
import requests
import time
from PIL import Image
from threading import Thread, Lock
from pathlib import Path
import torch
from models.common import DetectMultiBackend
from utils.general import (non_max_suppression, scale_boxes)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device
from utils.dataloaders import LoadImages

# Initialize YOLO model
def init_model():
    weights = 'C:/Users/duyng/Downloads/v5n_15k_46epoch/content/yolov5/runs/train/exp/weights/last.pt'
    device = select_device('')
    model = DetectMultiBackend(weights, device=device, data='data/coco128.yaml', fp16=False)
    stride, names, pt = model.stride, model.names, model.pt
    model.warmup(imgsz=(1, 3, 640, 640))  # Warmup
    print(f"Model initialized with classes: {names}")
    return model, stride, names

# YOLO Detection function
def detect_vehicles(image_path, model, stride, names, conf_thres=0.25, iou_thres=0.45):
    results = {}
    dataset = LoadImages(image_path, img_size=640, stride=stride)
    for path, img, im0s, vid_cap, _ in dataset:
        im = torch.from_numpy(img).to(model.device)
        im = im.half() if model.fp16 else im.float()
        im /= 255.0
        if len(im.shape) == 3:
            im = im[None]

        pred = model(im, augment=False, visualize=False)
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=None, agnostic=False, max_det=1000)

        annotator = Annotator(im0s, line_width=1, example=str(names))

        for det in pred:
            if len(det):
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0s.shape).round()
                for *xyxy, conf, cls in det:
                    cls_name = names[int(cls)]
                    results[cls_name] = results.get(cls_name, 0) + 1
                    label = f"{cls_name} {conf:.2f}"
                    annotator.box_label(xyxy, label, color=colors(int(cls), True))

        # Save the detected image
        cv2.imwrite(path, annotator.result())
    return results

# Traffic capture and detection loop
def capture_and_detect(path, model, stride, names, log_file, lock):
    count = 1
    directory = "data/images/trial"
    os.makedirs(directory, exist_ok=True)

    while True:
        try:
            url = path[2]
            headers = {"User-Agent": "Mozilla/5.0"}
            print(f"Loop {count}, Traffic captured at {time.ctime()} - {path[1]}")
            image_name = f"{path[0]}-{time.strftime('%Y_%m_%d_%H_%M_%S')}.jpg"
            image_path = os.path.join(directory, image_name)

            # Save image
            with open(image_path, 'wb') as f:
                f.write(requests.get(url, headers=headers).content)

            # Detect vehicles and save detected image
            detected_counts = detect_vehicles(image_path, model, stride, names)

             # Prepare log entry using `int()` for numeric counts
            log_parts = []
            for vehicle, count in detected_counts.items():
                try:
                    numeric_count = int(count)  # Ensure count is converted to an integer
                    log_parts.append(f"{vehicle} {numeric_count}")
                except ValueError:
                    print(f"Skipping non-numeric count for {vehicle}: {count}")

            # Log format: image_name: vehicle_type count, ...
            log_entry = f"{image_name}: " + ", ".join(log_parts) + "\n"

            # Write log
            with lock:  # Use lock to avoid race condition
                with open(log_file, 'a') as log:
                    log.write(log_entry)
            print(f"Loop {count}, {path[1]}: {detected_counts}")
            

        except Exception as e:
            print(f"Error in {path[1]}: {e}")
        
        time.sleep(20)
        count += 1

# Main function
def main():
    log_file = "vehicle_counts_log.txt"
    model, stride, names = init_model()
    lock = Lock()

    paths = [
        ["loc01", "Highway A1", "http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=58afea5dbd82540010390c4d&t=1667011700842"],
        ["loc02", "Vo Van Kiet", "http://giaothong.hochiminhcity.gov.vn:80/render/ImageHandler.ashx?id=56de42f611f398ec0c481296&t=1666752019191"],
        ["loc03","Vo Chi Cong","http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=5a8269c45058170011f6eae4"],
        ["loc04","Highway 13 - Pham Van Dong","http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=58affc6017139d0010f35cc8"],
        ["loc05","Long Thanh - Dau Giay Expressway","http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=5d9de43b766c880017188cb6&t=1667014633438"],
        ["loc06","Highway 22","http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=589b4379b3bf7600110283c9"],
        ["loc07","Highway 13 - Highway A1","http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=5874656eb807da0011e33cde&t=1667015665586"],
        ["loc08","Vo Thi Sau - Dinh Tien Hoang","http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=5a823e425058170011f6eaa4"]
    ]

    threads = []
    for path in paths:
        thread = Thread(target=capture_and_detect, args=(path, model, stride, names, log_file, lock))
        threads.append(thread)
        thread.start()
        time.sleep(0.2)
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
