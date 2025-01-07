
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def sum(array):
  result = 0
  for i in range(0,len(array)):
    result += array[0]
  return result

def getTraffic(date, destination):
    f = open('traffic/' + date + '.txt', 'r')
    cars = [0] * 15  # From 6 AM (index 0) to 9 PM (index 14)
    giants = [0] * 15
    bikes = [0] * 15

    for line in f:
        parts = line.split(": ")
        if len(parts) != 2:
            continue

        meta, counts_str = parts
        location = meta.split('-')[0]
        time_str = meta.split('-')[1].split('.')[0]
        time_parts = time_str.split('_')

        # Skip if destination doesn't match
        if (location != destination) and (destination != "all"):
            continue

        # Parse time components
        try:
            log_hour = int(time_parts[3])
        except (ValueError, IndexError):
            continue

        # Ensure the hour is within 6 AM to 9 PM
        if 6 <= log_hour < 21:
            index = log_hour - 6
        else:
            continue

        # Parse vehicle counts dynamically
        counts = counts_str.split(", ")
        for item in counts:
            try:
                vehicle, count = item.rsplit(" ", 1)
                count = int(count)
                if "car" in vehicle:
                    cars[index] += count
                elif "truck" in vehicle or "bus" in vehicle or "train" in vehicle:
                    giants[index] += count
                elif "motor" in vehicle or "bicycle" in vehicle:
                    bikes[index] += count
            except ValueError:
                continue

    f.close()
    return [cars, giants, bikes]


def getDate():
  date = []
  thisdir = os.getcwd()
  for r, d, f in os.walk(thisdir+"\\traffic"):
      for file in f:
          if file.endswith(".txt"):
              file = file.strip('.txt')
              file = '\t\t\t\t'+ file +'-2025'+'\t\t\t\t'
              date.append(file)
  return date

locationDict = {
  "01-Highway A1":"loc01",
  "02-Vo Van Kiet":"loc02",
  "03-Vo Chi Cong":"loc03",
  "04- Highway 13 - Pham Van Dong":"loc04",
  "05- Long Thanh - Dau Giay Expressway":"loc05",
  "06 - Highway 22":"loc06",
  "07- Vo Thi Sau - Dinh Tien Hoang":"loc08",
  "all locations":"all"
}