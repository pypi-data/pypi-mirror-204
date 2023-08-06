import uuid

from testtools.tools import get
from testtools.security import basic_auth, bearer

def test_get_basic_username():
    user = 'username'
    password = str(uuid.uuid4())
    data = get('authorization', basic_auth(user, password)).json()
    assert data['Basic']['user'] == user

def test_get_basic_password():
    user = 'username'
    password = str(uuid.uuid4())
    data = get('authorization', basic_auth(user, password)).json()
    assert data['Basic']['password'] == password
    
def test_get_bearer_token():
    token = str(uuid.uuid4())
    data = get('authorization', bearer(token)).json()
    assert data['Bearer'] == token