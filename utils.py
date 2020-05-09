import time
import lxc
from collections import OrderedDict

class LimitedSizeDict(OrderedDict):
    def __init__(self, *args, **kwds):
        self.size_limit = kwds.pop("size_limit", None)
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)

def search_between(content, start, end):
    return content[content.find(start) + len(start):content.rfind(end)]

def time_limit_lxc(container_name, time_limit):
    c = lxc.Container(container_name)
    start_time = time.time()
    while True:
        if (time.time() - start_time) > time_limit:
            if c.running:
                c.stop()
            return
        time.sleep(0.1)
