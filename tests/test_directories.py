#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import requests
import unittest
import wwwoman

url = "http://niouf.fr"
response1 = {"niouf":"niouf"}
response2 = {"niorf":"niorf"}

class TestWWWomanDirectories(unittest.TestCase):
    def setUp(self):
        wwwoman.wwwomanScenario.scenario_path = 'tests'
        
    @wwwoman.register_scenario("scenario.json")
    def test_scenario(self):
        r = requests.get(url)
        self.assertEqual(r.json(),response1)
        r = requests.get(url)
        self.assertEqual(r.json(),response2)
        r = requests.get("http://niorf.fr")
        self.assertEqual(r.content,"niouf")
