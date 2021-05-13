from pickle import load
from pathlib import Path


# https://stackoverflow.com/a/26209900
def pretty(value, htchar="    ", lfchar='\n', indent=0):
    nlch = lfchar + htchar * (indent + 1)
    if isinstance(value, dict):
        items = [
            nlch + repr(key) + ': ' + pretty(value[key], htchar, lfchar, indent + 1)
            for key in value
        ]
        return '{%s}' % (','.join(items) + lfchar + htchar * indent)
    elif isinstance(value, list):
        items = [
            nlch + pretty(item, htchar, lfchar, indent + 1)
            for item in value
        ]
        return '[%s]' % (','.join(items) + lfchar + htchar * indent)
    elif isinstance(value, tuple):
        items = [
            nlch + pretty(item, htchar, lfchar, indent + 1)
            for item in value
        ]
        return '(%s)' % (','.join(items) + lfchar + htchar * indent)
    else:
        return repr(value)


data_path = str(Path(__file__).parent.absolute()) + "/../data/sleep_tracker_data.pickle"

try:
    f = open(data_path, "rb")
    data = load(f)
    f.close()
    print(pretty(data))
except FileNotFoundError:
    exit("未找到 sleep_tracker_data.pickle")
