import pytest

@pytest.mark.api
@pytest.mark.smoke
def test_health_schema(api,base_url):
    body=api.get(base_url+'/health').json();assert body['status']=='healthy';assert isinstance(body['bug_mode'],bool)

@pytest.mark.api
def test_registration_contract(api,base_url,registered):
    assert registered['token']
    r=api.post(base_url+'/api/auth/register',json=registered['data'])
    assert r.status_code==409 and isinstance(r.json()['detail'],str)

@pytest.mark.api
def test_service_contract(api,base_url):
    r=api.get(base_url+'/api/services');assert r.status_code==200
    for item in r.json():
        assert {'id','name','category','description','duration_minutes','price','active'}<=item.keys()
        assert isinstance(item['id'],int) and item['duration_minutes']>=15

@pytest.mark.api
@pytest.mark.security
def test_protected_contract(api,base_url): assert api.get(base_url+'/api/bookings/me').status_code==401

@pytest.mark.api
def test_invalid_payload_contract(api,base_url):
    r=api.post(base_url+'/api/auth/register',json={'email':'not-an-email'})
    assert r.status_code==422 and isinstance(r.json()['detail'],list)
