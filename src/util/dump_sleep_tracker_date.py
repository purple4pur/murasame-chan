from pickle import load
from json import dumps
from pathlib import Path


data_path = str(Path(__file__).parent.absolute()) + "/../data/sleep_tracker_data.pickle"

try:
    f = open(data_path, "rb")
    data = load(f)
    f.close()
    print(dumps(data, indent=4))
except FileNotFoundError:
    exit("未找到 sleep_tracker_data.pickle")
