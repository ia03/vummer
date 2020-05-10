import time
import lxc
from collections import OrderedDict
from judge0api.status import Judge0Status

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

def get_log_filename(container_name):
    return 'logs/' + container_name + '.log'

def get_code(args):
    if '```' in args:
        code = search_between(args, '```', '```')
    else:
        code = args
    return code
