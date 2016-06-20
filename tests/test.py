#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import json
import requests
import unittest
import httpretty
import wwwoman

url = "http://niouf.fr"
response1 = {"niouf":"niouf"}
response2 = {"niorf":"niorf"}
response3 = {"niorf":"niorf1"}

class TestWWWoman(unittest.TestCase):
    def setUp(self):
        wwwoman.wwwomanScenario.reset_scenario_path()

    @wwwoman.register(uri=url,template="tests/test.json",content_type="application/json")
    def test_templateFile(self):
        r = requests.get(url)
        self.assertEqual(r.json(),response1)

    @wwwoman.register(uri=url,body=json.dumps(response2),content_type="application/json")
    def test_body(self):
        r = requests.get(url)
        self.assertEqual(r.json(),response2)

    @wwwoman.register(uri='niouf.html',body=json.dumps(response2),content_type="application/json",baseuri=url)
    def test_baseuri(self):
        r = requests.get(url+'/niouf.html')
        self.assertEqual(r.json(),response2)

    @wwwoman.register(uri=url,template=["tests/test.json",{"body":json.dumps(response2)}],content_type="application/json")
    def test_templateDouble(self):
        r = requests.get(url)
        self.assertEqual(r.json(),response1)
        r = requests.get(url)
        self.assertEqual(r.json(),response2)

    @httpretty.activate
    def test_function(self):
        wwwoman.wwwoman.register_uri(uri=url,template=["tests/test.json",{"body":json.dumps(response2)}],content_type="application/json")
        r = requests.get(url)
        self.assertEqual(r.json(),response1)
        r = requests.get(url)
        self.assertEqual(r.json(),response2)

    @wwwoman.register_scenario("tests/scenario.json")
    def test_scenario(self):
        r = requests.get(url)
        self.assertEqual(r.json(),response1)
        r = requests.get(url)
        self.assertEqual(r.json(),response2)
        r = requests.get("http://niorf.fr")
        self.assertEqual(r.content,"niouf")

    @wwwoman.register_scenario("tests/scenario_with_templatedir.json")
    def test_scenario_with_templatedir(self):
        r = requests.get(url)
        self.assertEqual(r.json(),response1)
        r = requests.get(url)
        self.assertEqual(r.json(),response2)
        r = requests.get("http://niorf.fr")
        self.assertEqual(r.content,"niouf")

    @wwwoman.register_scenario("tests/scenario_with_baseuri.json")
    def test_scenario_with_baseuri_in_scenario_file(self):
        r = requests.get(url + '/test.html')
        self.assertEqual(r.json(),response1)
        r = requests.get(url + '/test.html')
        self.assertEqual(r.json(),response2)
        r = requests.get("http://niorf.fr")
        self.assertEqual(r.content,"niouf")

    @wwwoman.register_scenario(
        "tests/scenario_with_baseuri_as_parameter.json",
        baseuri='http://niouf.fr'
    )
    def test_scenario_with_baseuri_as_parameter(self):
        r = requests.get(url + '/test.html')
        self.assertEqual(r.json(),response1)
        r = requests.get(url + '/test.html')
        self.assertEqual(r.json(),response2)
        r = requests.get("http://niorf.fr")
        self.assertEqual(r.content,"niouf")

    @wwwoman.register_scenario("tests/scenario_with_include.json")
    def test_scenario_with_include(self):
        r = requests.get(url + '/test.html')
        self.assertEqual(r.json(),response1)
        r = requests.get(url + '/test.html')
        self.assertEqual(r.json(),response2)
        r = requests.get("http://niorf.fr")
        self.assertEqual(r.content,"niouf")
        r = requests.get('http://plouf.fr/test.html')
        self.assertEqual(r.json(),response1)
        r = requests.get('http://plouf.fr/test.html')
        self.assertEqual(r.json(),response3)
        r = requests.get("http://niorf.fr")
        self.assertEqual(r.content,"niouf")

@wwwoman.register(uri=url,body=json.dumps(response2),content_type="application/json")
def test_function():
    r = requests.get(url)
    assert(r.json()==response2)
