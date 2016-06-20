#!/usr/bin/env python
#encoding:utf-8
"""
Created on 19 June 2016
@author: Brice GRICHY
"""
from __future__ import unicode_literals

import os
import json
import functools
import httpretty
from .WWWoman import wwwoman, _translatePath

class wwwomanScenario(object):
    """
    The scenario registration class
    """
    scenario_path = os.getcwd()
    """
    Directory for scenario files (Default: ``os.getcwd()``)
    """

    @classmethod
    def register_scenario(self,filename,baseuri=None):
        """
        Register all URI described in scenario file.

        :param filename: path to scenario file. If the path is relative, use\
        ``scenario_path`` attribute for base directory (defaulted to working\
        directory)
        :type filename: string
        :param baseuri: base uri used when scenario file contains path as\
        ``uri``
        :type baseuri: string

        .. warning:: ``baseuri`` indicated in scenario file is prior over\
        ``baseuri`` parameter

        .. seealso:: Scenario file syntax
        """
        filename = _translatePath(self.scenario_path,filename)
        with open(filename,'r') as fd:
            script = json.load(fd)
        if baseuri is None:
            if 'baseuri' in script.keys():
                baseuri = script['baseuri']
        if 'templatedir' in script.keys():
            templatedir = script['templatedir']
        else:
            templatedir = None
        if 'includes' in script.keys():
            for item in script['includes']:
                self.register_scenario(item)

        for _item in script['uriList']:
            item = dict()
            item.update(_item)
            if 'baseuri' not in item.keys() or item['baseuri'] is None:
                item['baseuri'] = baseuri
            if 'templatedir' not in item.keys() or item['templatedir'] is None:
                item['templatedir'] = templatedir
            wwwoman.register_uri(**item)

    @classmethod
    def reset_scenario_path(self):
        """
        Reset value of ``scenario_path`` to working directory
        """
        self.scenario_path = os.getcwd()

def register_scenario(filename,baseuri=None):
    """
    Decorator for scenario registration

    .. seealso:: :class:`register_scenario <wwwoman.wwwomanScenario.register_scenario>` for\
    parameters
    """
    def decorator(func):
        @functools.wraps(func)
        @httpretty.activate
        def test_wrapped(*args,**kw):
            wwwomanScenario.register_scenario(filename,baseuri=baseuri)
            return func(*args,**kw)
        return test_wrapped
    return decorator
