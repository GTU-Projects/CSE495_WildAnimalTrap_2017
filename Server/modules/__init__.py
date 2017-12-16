import os,sys

MODULES_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,MODULES_PATH)

SERVER_PATH = os.path.dirname(MODULES_PATH)

PROJECT_DIR_PATH = os.path.dirname(SERVER_PATH)
sys.path.insert(0,PROJECT_DIR_PATH+"/SharedData")

print("Modules__init__")