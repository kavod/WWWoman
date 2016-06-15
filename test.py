import json
import requests
import unittest
import httpretty
import copy

url = "http://niouf.fr"
response1 = {"niouf":"niouf"}
response2 = {"niorf":"niorf"}

def WWWomanScenario(filename):
    with open(filename,'r') as fd:
        script = json.load(fd)
    item = script['uriList'][0]
    def _myDecorator1(func):
        item = script['uriList'].pop(0)
        def wrapped1(cls):
            return WWWoman(**item)(func)(cls)
        if len(script['uriList'])>0:
            return _myDecorator1(wrapped1)
        else:
            return wrapped1
    return _myDecorator1

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
    def _myDecorator2(func):
        @httpretty.activate
        def wrapped2(cls):
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
            return func(cls)
        return wrapped2
    return _myDecorator2

class Test1(unittest.TestCase):
    @WWWoman(uri=url,template="test.json",content_type="application/json")
    def test_1(self):
        r = requests.get(url)
        self.assertEqual(r.json(),response1)

    @WWWoman(uri=url,body=json.dumps(response2),content_type="application/json")
    def test_2(self):
        r = requests.get(url)
        self.assertEqual(r.json(),response2)

    @WWWoman(uri=url,template=["test.json",{"body":json.dumps(response2)}],content_type="application/json")
    def test_3(self):
        r = requests.get(url)
        self.assertEqual(r.json(),response1)
        r = requests.get(url)
        self.assertEqual(r.json(),response2)

    @WWWomanScenario("scenario1.json")
    def test_4(self):
        print(httpretty.httpretty._entries)
        r = requests.get(url)
        self.assertEqual(r.json(),response1)
        r = requests.get(url)
        self.assertEqual(r.json(),response2)
        r = requests.get("http://niorf.fr")
        self.assertEqual(r.content,"niouf")
