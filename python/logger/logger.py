import time


class Logger:
    def __init__(self, name):
        self.name = name

    def info(self, message):
        print("{}: [{}] -> {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), self.name, message))
