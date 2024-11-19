!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="DpNtkiVrdlmwXlWXhs67")
project = rf.workspace("school-uov28").project("vechile-detect-and-counting-txbmn")
version = project.version(4)
dataset = version.download("yolov5")
                