import os
from collections import defaultdict

# Directory containing the label files
label_dir = "C:/Users/duyng/Desktop/Vehicle_Counting/projectTraffic-main/data/Vietnamese vehicle.v3i.yolov5pytorch/train/labels"  # Replace with the path to your label files

# Initialize a dictionary to store counts of each class
class_counts = defaultdict(int)

# Go through each label file
for filename in os.listdir(label_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(label_dir, filename), "r") as file:
            for line in file:
                # Get the class name (first element of each line)
                class_name = line.strip().split()[0]
                # Increment the count for this class
                class_counts[class_name] += 1

# Print the quantity of each class
print("Class quantities:")
for class_name, count in class_counts.items():
    print(f"{class_name}: {count}")
