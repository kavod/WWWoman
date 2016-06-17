# WWWoman

WWWoman is an extension of the [httpretty] client mocking tool

## Simple use
You can directly register URI using decorator like this:
```
import requests
from WWWoman import WWWoman

@WWWoman(uri="http://test.com",method='GET',body='test')
def test_wwwoman():
    r=requests.get("http://test.com")
    assert(r.content=='test')
```
Compatible with nosetests :
```
$ nosetests
.
----------------------------------------------------------------------
Ran 1 test in 0.016s

OK
```
or with unittest.

## Template management
Instead pushing the body from a string, you can use ``template`` parameter in order to indicate a file (flat or binary).
Example with ``test.html`` containing `my test` string (and final newline) as content:
```
import requests
from WWWoman import WWWoman

@WWWoman(uri="http://test.com",method='GET',template='test.html')
def test_wwwoman():
    r=requests.get("http://test.com")
    assert(r.content=='my test\n')
```

## Scenario management
When you write a really large number of unit tests, you may want define scenarios with a set of several uri to mock.
For this, WWWomanScenario decorator is available:
**scenario.json**
```
{
  "description": "blah blah blah",
  "uriList":[
    {
      "uri": "http://niouf.fr",
      "template":[
        "test.html",
        {
          "body":"niouf niouf"
        }
      ],
      "content_type":"application/json"
    },
    {
      "uri": "http://niorf.fr",
      "body": "niouf"
    }
  ]
}
```
You can see that template parameter is a list. In this case, registered uri (niouf.fr) will first give the content of test.json ('my test') then, the next call will response 'niouf niouf'.

Let's use with WWWomanScenario:
```
import requests
from WWWoman import WWWomanScenario

@WWWomanScenario('scenario.json')
def test_wwwoman():
    r=requests.get("http://niouf.fr")
    assert(r.content=='my test\n')
    r=requests.get("http://niouf.fr")
    assert(r.content=='niouf niouf')
    r=requests.get("http://niouf.fr")
    assert(r.content=='niouf niouf')
    r=requests.get("http://niorf.fr")
    assert(r.content=='niouf')
```

[httpretty]: https://github.com/gabrielfalcao/HTTPretty
