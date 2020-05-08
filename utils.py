#!/usr/bin/env python

import time
import lxc

def search_between(content, start, end):
    return content[content.find(start) + len(start):content.rfind(end)]

def time_limit_lxc(container_name, time_limit):
    c = lxc.Container(container_name)
    start_time = time.time()
    while True:
        if (time.time() - start_time) > time_limit and c.running:
            c.kill()
            return
        time.sleep(0.1)
