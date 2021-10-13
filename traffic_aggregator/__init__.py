import time


def log(func):
    def wrapper(*args, **kwargs):
        ts = time.time()
        print("Start {functionName}".format(functionName=func.__name__))
        result = func(*args, **kwargs)
        tf = time.time()
        print("Finish {functionName}: Time: {timeInMillis} ms.".format(functionName=func.__name__,
                                                                       timeInMillis=round((tf - ts) * 1000, 1)))
        return result

    return wrapper
