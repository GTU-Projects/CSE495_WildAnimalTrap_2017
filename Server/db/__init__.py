import os,sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,PATH)

SERVER_PATH = os.path.dirname(PATH)

PROJECT_DIR_PATH = os.path.dirname(SERVER_PATH)
sys.path.insert(0,PROJECT_DIR_PATH+"/SharedData")

print("DB__init__")