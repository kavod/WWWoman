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
        def test_wrapped(cls):
            for item in script['uriList']:
                WWWoman.wwwoman(**item)
            return func(cls)
        return test_wrapped
    return decorator
