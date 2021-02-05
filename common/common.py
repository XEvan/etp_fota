from functools import wraps


class Singleton(type):
    import threading
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


def RILPrint(func):
    from logger import rfic_info
    @wraps(func)
    def ril_print(*args, **kwargs):
        rfic_info("[Func Call] <%s>开始执行..." % func.__name__, log=False)
        res = func(*args, **kwargs)
        args = "" if len(args) == 0 else args
        kwargs = "" if len(kwargs) == 0 else kwargs
        rfic_info("[Func Call] <%s>%s%s------>%s" % (func.__name__, str(args), str(kwargs), res), log=False)
        return res

    return ril_print
