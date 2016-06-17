#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import httpretty

def WWWoman(
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
    **headers
):
    def decorator(func):
        # wrapper name begins by test_ in order to be recognized by nosetests
        @httpretty.activate
        def test_wrapped(*args,**kw):
            wwwoman(
                template=template,
                method=method,
                uri=uri,
                body=body,
                adding_headers=adding_headers,
                forcing_headers=forcing_headers,
                status=status,
                responses=responses,
                match_querystring=match_querystring,
                priority=priority,
                headers=headers
            )
            return func(*args,**kw)
        return test_wrapped
    return decorator

def wwwoman(
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
    **headers):
    if template is not None:
        if isinstance(template,list):
            responses = []
            for item in template:
                if isinstance(item,basestring):
                    with open(item,'rb') as fd:
                        body=fd.read()
                    responses.append(httpretty.Response(body=body))
                elif isinstance(item,dict):
                    responses.append(httpretty.Response(**item))
        else:
            with open(template,'rb') as fd:
                body=fd.read()
    httpretty.register_uri(
        method=method,
        uri=uri,
        body=body,
        adding_headers=adding_headers,
        forcing_headers=forcing_headers,
        status=status,
        responses=responses,
        match_querystring=match_querystring,
        priority=priority,
        headers=headers
    )
