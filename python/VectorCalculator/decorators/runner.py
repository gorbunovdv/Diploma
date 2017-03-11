# coding=utf-8
import resource
import time
from functools import wraps
from threading import Thread

result = None


def time_consumption(function):
    """
    Декоратор измеряет время работы функции function.
    :param function: функция, время работы которой нужно измерить
    """
    @wraps(function)
    def new_function(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        print ("Total running time is %.3f seconds" % (end_time - start_time))
        return result

    return new_function


def memory_consumption(function):
    """
    Декоратор измеряет потребление памяти функцией function.
    :param function: функция, потребление памяти измерить
    """
    def run(func, *args, **kwargs):
        global result
        result = func(*args, **kwargs)

    def runner(*args, **kwargs):
        global result
        start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        max_memory = 0
        t = Thread(target=run, args=tuple([function] + list(args)), kwargs=kwargs)
        t.start()
        while t.isAlive():
            current_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if max_memory < current_memory - start_memory:
                max_memory = current_memory - start_memory
            time.sleep(0.1)
        t.join()
        print ("Total memory consumed is %.3f mb" % (max_memory / 1024.0 / 1024))
        return result

    return runner
