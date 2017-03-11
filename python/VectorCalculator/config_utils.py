import json

config = None


def init_config(args):
    global config
    path = "config.json"
    if len(args) > 1:
        path = args[1]
    config = json.loads(open(path).read())
