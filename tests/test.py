#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import json
import requests
import unittest
import httpretty
import WWWoman

url = "http://niouf.fr"
response1 = {"niouf":"niouf"}
response2 = {"niorf":"niorf"}

class TestWWWoman(unittest.TestCase):
    @WWWoman.WWWoman(uri=url,template="test.json",content_type="application/json")
    def test_templateFile(self):
        r = requests.get(url)
        self.assertEqual(r.json(),response1)

    @WWWoman.WWWoman(uri=url,body=json.dumps(response2),content_type="application/json")
    def test_body(self):
        r = requests.get(url)
        self.assertEqual(r.json(),response2)

    @WWWoman.WWWoman(uri=url,template=["test.json",{"body":json.dumps(response2)}],content_type="application/json")
    def test_templateDouble(self):
        r = requests.get(url)
        self.assertEqual(r.json(),response1)
        r = requests.get(url)
        self.assertEqual(r.json(),response2)

    @httpretty.activate
    def test_function(self):
        WWWoman.wwwoman(uri=url,template=["test.json",{"body":json.dumps(response2)}],content_type="application/json")
        r = requests.get(url)
        self.assertEqual(r.json(),response1)
        r = requests.get(url)
        self.assertEqual(r.json(),response2)

    @WWWoman.WWWomanScenario("scenario1.json")
    def test_scenario(self):
        r = requests.get(url)
        self.assertEqual(r.json(),response1)
        r = requests.get(url)
        self.assertEqual(r.json(),response2)
        r = requests.get("http://niorf.fr")
        self.assertEqual(r.content,"niouf")
print(TestWWWoman.test_scenario.__name__)
