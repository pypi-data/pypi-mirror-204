from testtools.tools import get

def test_get():
    data = get('request').json()
    assert len(data) == 1

def test_accepts_when_not_valid_content_type_returns_415():
    status = get('request/accepts', {'Content-Type': 'non_valid'}).status_code
    assert status == 415

def test_accepts_when_valid_content_type_returns_200():
    status = get('request/accepts', {'Content-Type': 'text/plain'}).status_code
    assert status == 200
    
def test_validates_request_when_invalid_returns_400():
    url = 'request/validates-request'
    headers = {}
    status = get(url, headers).status_code
    assert status == 400

def test_validates_request_when_valid_returns_200():
    url = 'request/validates-request'
    headers = {'TestHeader': 'test-header-value'}
    status = get(url, headers).status_code
    assert status == 200
    
def test_requires_parameters_when_invalid_returns_400():
    url = 'request/requires-parameters'
    status = get(url).status_code
    assert status == 400

def test_requires_parameters_when_valid_returns_200():
    url = 'request/requires-parameters?testParameter=1'
    status = get(url).status_code
    assert status == 200

def test_accepts_json_when_invalid_returns_415():
    url = 'request/accepts-json'
    headers = {'Content-Type': 'application/xml'}
    status = get(url, headers).status_code
    assert status == 415

def test_accepts_json_when_valid_returns_200():
    url = 'request/accepts-json'
    headers = {'Content-Type': 'application/json'}
    status = get(url, headers).status_code
    assert status == 200