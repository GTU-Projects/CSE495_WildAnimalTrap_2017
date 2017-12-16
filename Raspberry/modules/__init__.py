import os,sys

MODULE_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,MODULE_DIR_PATH)

RASPBERRY_DIR_PATH= os.path.dirname(MODULE_DIR_PATH)
PROJECT_DIR_PATH = os.path.dirname(RASPBERRY_DIR_PATH)

sys.path.insert(0,PROJECT_DIR_PATH+"/SharedData/")

print("Modules__init__")