import threading, logging

logger = logging.getLogger(__name__)

class MyThread(threading.Thread):
    
    def __init__(self, func, *arg, **kwargs):
        self.func = func
        self.arg = arg
        self.kwargs = kwargs
        threading.Thread.__init__(self)
        
    def run(self):
        logger.info('Performing tasks')
        self.func(*self.arg, **self.kwargs)