!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="DpNtkiVrdlmwXlWXhs67")
project = rf.workspace("vccohexa").project("vc_cohexa_batch1")
version = project.version(4)
dataset = version.download("yolov5")
                