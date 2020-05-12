import time
from collections import OrderedDict
from json import JSONEncoder

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

def get_code_from_text(arg):
    if '```' in arg:
        code = search_between(arg, '```', '```')
    else:
        code = arg
    return code

def get_code(arg, attachment):
    if attachment:
        return attachment
    else:
        return get_code_from_text(arg).encode()

def stats(sub_time, sub_mem):
    if sub_time and sub_mem:
        return ('CPU time: ' + str(sub_time) + ' s, '
            + 'Memory usage: ' + str(sub_mem) + ' kB\n')
    else:
        return ''
