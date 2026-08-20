import os
import pytest
import requests

@pytest.fixture(scope='session')
def base_url():
    return os.getenv('API_BASE_URL','http://localhost:8000')

@pytest.fixture(scope='session')
def api(base_url):
    try:
        requests.get(base_url+'/health',timeout=2).raise_for_status()
    except requests.RequestException:
        pytest.skip('Live ServiceHub API is not running')
    return requests.Session()

@pytest.fixture
def registered(api,base_url):
    import uuid
    data={'name':'Automation User','email':f'api-{uuid.uuid4()}@example.com','password':'Strong123!'}
    created=api.post(base_url+'/api/auth/register',json=data)
    assert created.status_code==201
    assert 'access_token' not in created.json()
    login=api.post(base_url+'/api/auth/login',json={'email':data['email'],'password':data['password']})
    assert login.status_code==200
    return {'token':login.json()['access_token'],'data':data}
