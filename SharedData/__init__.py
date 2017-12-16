import os,sys

SHARED_DATA_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,SHARED_DATA_PATH)

print("SharedData__init__")