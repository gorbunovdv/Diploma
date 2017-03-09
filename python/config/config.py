import json
import sys

config = None


def load_config(path):
    global config
    config = json.loads(open(path).read())


load_config(sys.argv[1])
