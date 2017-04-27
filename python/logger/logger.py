# coding=utf-8

import time
import multiprocessing

from datetime import datetime

"""
    Класс для удобного логирования на экран
"""
class Logger:
    def __init__(self, name):
        self.name = name

    def info(self, message):
        print("{}: [{}] -> {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), self.name, message))

"""
    Класс для удобного вывода прогресса на экран
"""
class Ticker:
    lock = multiprocessing.Lock()

    def __init__(self, logger, max_ticks, name, step=10000):
        self.logger = logger
        self.max_ticks = max_ticks
        self.name = name

        self.current_ticks = 0
        self.start_time = datetime.now()
        self.step = step

    def __call__(self):
        with Ticker.lock:
            self.current_ticks += 1
            if (self.max_ticks == 0 and self.current_ticks % self.step == 0) or (self.max_ticks != 0 and self.current_ticks % (self.max_ticks // 1000) == 0):
                self.log()

    def log(self):
        seconds = (datetime.now() - self.start_time).total_seconds()
        if self.max_ticks != 0:
            self.logger.info("[{}]: {}/{} ticks are finished ({} per second, one in {} seconds, estimated time is {} seconds)"
                             .format(self.name, self.current_ticks, self.max_ticks,
                                     1. * self.current_ticks / seconds, 1. * seconds / self.current_ticks,
                                     (self.max_ticks - self.current_ticks) / (1. * self.current_ticks / seconds)))
        else:
            self.logger.info("[{}]: {} ticks are finished ({} per second, one in {} seconds)"
                             .format(self.name, self.current_ticks,
                                     1. * self.current_ticks / seconds, 1. * seconds / self.current_ticks))

"""
    Генератор для удобного вывода прогресса по iterable на экран
"""
def IterableTicker(logger, iterable, step=10000):
    ticker = Ticker(logger, 0, type(iterable).__name__, step)
    for object in iterable:
        yield object
        ticker()
