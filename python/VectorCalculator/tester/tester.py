from decorators.runner import memory_consumption, time_consumption


def test_two_functions(model_, function1, function2, evaluator, printer, *args, **kwargs):
    @time_consumption
    def f1(*args, **kwargs):
        return function1(*args, **kwargs)

    @time_consumption
    def f2(*args, **kwargs):
        return function2(*args, **kwargs)

    print "Running first function: ", function1.__name__
    result1 = f1(*args, **kwargs)
    print "Finished running first function: ", function1.__name__
    fresult1 = open(function1.__name__, "w")
    printer(model_, result1, fresult1)
    fresult1.close()
    print "Running second function: ", function2.__name__
    result2 = f2(*args, **kwargs)
    print "Finished running second function: ", function2.__name__
    fresult2 = open(function2.__name__, "w")
    printer(model_, result2, fresult2)
    fresult2.close()
    print "Evaluating results: ", evaluator.__name__
    evaluator(result1, result2)
    return result1, result2


def test_single_function(model, function, printer, *args, **kwargs):
    @time_consumption
    def f(*args, **kwargs):
        return function(*args, **kwargs)

    print "Running single function: ", function.__name__
    result = f(*args, **kwargs)
    fresult = open(function.__name__, "w")
    printer(model, result, fresult)
    fresult.close()
    return result
