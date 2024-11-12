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
