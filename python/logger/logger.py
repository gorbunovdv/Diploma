import time

from datetime import datetime


class Logger:
    def __init__(self, name):
        self.name = name

    def info(self, message):
        print("{}: [{}] -> {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), self.name, message))

class Ticker:
    def __init__(self, logger, max_ticks, name):
        self.logger = logger
        self.max_ticks = max_ticks
        self.name = name

        self.current_ticks = 0
        self.start_time = datetime.now()

    def __call__(self):
        self.current_ticks += 1
        if self.current_ticks % (self.max_ticks // 1000) == 0:
            self.log()

    def log(self):
        seconds = (datetime.now() - self.start_time).total_seconds()
        if self.max_ticks is not None:
            self.logger.info("[{}]: {}/{} ticks are finished ({} per second, one in {} seconds, estimated time is {} seconds)"
                             .format(self.name, self.current_ticks, self.max_ticks,
                                     1. * self.current_ticks / seconds, 1. * seconds / self.current_ticks,
                                     (self.max_ticks - self.current_ticks) / (1. * self.current_ticks / seconds)))
        else:
            self.logger.info("[{}]: {} ticks are finished ({} per second, one in {} seconds)"
                             .format(self.name, self.current_ticks,
                                     1. * self.current_ticks / seconds, 1. * seconds / self.current_ticks))
