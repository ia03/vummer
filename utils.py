#!/usr/bin/env python

def search_between(content, start, end):
    return content[content.find(start) + len(start):content.rfind(end)]
