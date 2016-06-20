#!/usr/bin/env python
#encoding:utf-8
"""
Created on 19 June 2016
@author: Brice GRICHY
"""

from __future__ import unicode_literals

import os
import functools
import urlparse
import httpretty

def _translatePath(root_path,path):
    if not os.path.isabs(root_path):
        root_path = os.path.abspath(root_path)
    if not os.path.isabs(path):
        return os.path.join(root_path,path)
    else:
        return path

class wwwoman(httpretty.httpretty):
    """
    The URI registration class
    """

    template_path=os.getcwd() #: Niorf
    """
    Base directory for scenario files (default: ``os.getcwd``)
    """

    @classmethod
    def register_uri(self,
        uri,
        body='WWWoman 8)',
        template=None,
        method=httpretty.GET,
        adding_headers=None,
        forcing_headers=None,
        status=200,
        responses=None,
        match_querystring=False,
        priority=0,
        baseuri=None,
        templatedir=None,
        **headers):
        """
        Register a new URI.
        Parameters are the same than ``register_uri`` method of httpretty class\
        except the extra parameters below

        .. seealso:: \
        `httpretty documentation <https://github.com/gabrielfalcao/HTTPretty>`_\
        for regular parameters of ``register_uri``

        :param template: ``template`` can be a path or a list of path to a \
        template file.\
        If template is not None, the ``body`` or the ``responses`` parameters\
        will be ignored in favor of the content of the template file(s).

        :type template: string or list of strings

        :type baseuri: string
        
        :param baseuri: if ``baseuri`` is not None, relative uri path could be\
        entered instead of complete URI.

        .. note:: if ``uri`` is an absolute uri, the ``baseuri`` is ignored

        :param templatedir: if ``templatedir`` is note None, ``template``\
        relative path will be used as base instead of working directory (cwd)
        :type templatedir: string

        :Example:

        >>> import httpretty
        >>> import requests
        >>> import wwwoman
        >>> httpretty.httpretty.enable()
        >>> # Normal use:
        >>> wwwoman.wwwoman.register_uri(uri="http://test.io",body="My test!")
        >>> requests.get('http://test.io').content
        'My test!'
        >>> # Use of ``baseuri`` parameter
        >>> wwwoman.wwwoman.register_uri(
                uri='test.html',
                baseuri='http://test.io',
                body="My second test"
            )
        >>> requests.get('http://test.io/test.html').content
        'My second test'
        >>> # Use of ``template`` parameter
        >>> ## test.io will return the content of ``tests/templates/index.html``
        >>> wwwoman.wwwoman.register_uri(
                uri='http://test.io',
                template='index.html',
                templatedir='tests/templates'
            )
        'The index.html content'
        """
        if templatedir is None:
            templatedir = self.template_path
        if template is not None:
            if isinstance(template,list):
                responses = []
                for item in template:
                    if isinstance(item,basestring):
                        item = _translatePath(templatedir,item)
                        with open(item,'rb') as fd:
                            body=fd.read()
                        responses.append(httpretty.Response(body=body))
                    elif isinstance(item,dict):
                        responses.append(httpretty.Response(**item))
            else:
                template = _translatePath(templatedir,template)
                with open(template,'rb') as fd:
                    body=fd.read()

        httpretty.register_uri(
            method=method,
            uri=urlparse.urljoin(baseuri,uri),
            body=body,
            adding_headers=adding_headers,
            forcing_headers=forcing_headers,
            status=status,
            responses=responses,
            match_querystring=match_querystring,
            priority=priority,
            headers=headers
        )

class wwwomanized(object):
    """
    The context manager class
    ..seealso: wwwoman.register_uri for parameters
    """
    def __init__(self,
        uri,
        body='WWWoman 8)',
        template=None,
        method=httpretty.GET,
        adding_headers=None,
        forcing_headers=None,
        status=200,
        responses=None,
        match_querystring=False,
        priority=0,
        templatedir=None,
        **headers
    ):
        self.uri = uri
        self.body = body
        self.template = template
        self.method = method
        self.adding_headers=adding_headers
        self.forcing_headers=forcing_headers
        self.status=status
        self.responses=responses
        self.match_querystring = match_querystring
        self.priority=priority
        self.headers=headers
        self.templatedir = templatedir

    def __enter__(self):
        wwwoman.register_uri(
            template=self.template,
            method=self.method,
            uri=self.uri,
            body=self.body,
            adding_headers=self.adding_headers,
            forcing_headers=self.forcing_headers,
            status=self.status,
            responses=self.responses,
            match_querystring=self.match_querystring,
            priority=self.priority,
            templatedir=self.templatedir,
            **self.headers
        )

    def __exit__(self, exc_type, exc_value, traceback):
        httpretty.reset()

def register(*reg_args,**reg_kw):
    """
    The WWWoman decorator.

    .. seealso:: :class:`wwwoman.register_uri <wwwoman.wwwoman.register_uri>` for parameters

    .. note:: This decorator includes httpretty.enable. No need to import\
    httpretty to make it working.

    :Example:

    >>> import unittest
    >>> import wwwoman
    >>> class MyTest(unittest.TestCase):
    ...     def setUp(self):
    ...         wwwoman.wwwoman.templatedir = 'tests/tmp'
    ...
    ...     @wwwoman.register(uri='http://test.io',template='file1.html')
    ...     def test_example(self):
    ...         r = requests.get('http://test.io')
    ...         self.assertEquals(r.content,open('tests/tmp/file1.html').read())
    """
    def decorator(test):
        @functools.wraps(test)
        @httpretty.activate
        def wrapper(*args,**kw):
            with wwwomanized(*reg_args,**reg_kw):
                return test(*args, **kw)
        return wrapper

    return decorator
