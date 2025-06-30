import threading

class AsyncWrapper(object):
    def __init__(self, func, *args, **kwargs):
        self._result = None
        self._ready = threading.Event()
        self._thread = threading.Thread(target=self._run, args=(func, args, kwargs))
        self._thread.start()

    def _run(self, func, args, kwargs):
        self._result = func(*args, **kwargs)
        self._ready.set()

    def await_result(self):
        self._ready.wait()
        return self._result
    
def make_async_func(method):
    def wrapper(*args, **kwargs):
        return AsyncWrapper(method, *args, **kwargs)
    return wrapper