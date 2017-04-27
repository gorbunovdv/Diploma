# coding=utf-8

import json
import sys

config = None

"""
    Функция загружает JSON-конфиг из файла с путем path
"""
def load_config(path):
    global config
    config = json.loads(open(path).read())


load_config(sys.argv[1])
