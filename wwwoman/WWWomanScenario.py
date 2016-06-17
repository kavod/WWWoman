#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import json
import httpretty
import WWWoman

def WWWomanScenario(filename):
    with open(filename,'r') as fd:
        script = json.load(fd)
    def decorator(func):
        @httpretty.activate
        def test_wrapped(*args,**kw):
            for item in script['uriList']:
                WWWoman.wwwoman(**item)
            return func(*args,**kw)
        return test_wrapped
    return decorator
