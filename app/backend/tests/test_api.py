from datetime import datetime,timedelta
import pytest

@pytest.mark.smoke
def test_health(client): assert client.get('/health').json()['status']=='healthy'

@pytest.mark.api
def test_duplicate_registration_is_rejected(client):
    data={'name':'Duplicate User','email':'duplicate@example.com','password':'Strong123!'}
    assert client.post('/api/auth/register',json=data).status_code==201
    r=client.post('/api/auth/register',json=data)
    assert r.status_code==409 and 'already' in r.json()['detail']

@pytest.mark.api
@pytest.mark.parametrize('password',["short","onlyletters","12345678"])
def test_weak_password_validation(client,password):
    assert client.post('/api/auth/register',json={'name':'QA','email':f'{password}@example.com','password':password}).status_code==422

@pytest.mark.smoke
def test_login_and_list_services(client):
    login=client.post('/api/auth/login',json={'email':'admin@servicehub.example','password':'Admin123!'})
    assert login.status_code==200 and login.json()['token_type']=='bearer'
    services=client.get('/api/services').json()
    assert len(services)>=3 and all(x['active'] for x in services)

@pytest.mark.api
def test_search_is_case_insensitive(client):
    assert any(x['name']=='Massage' for x in client.get('/api/services?search=MASSAGE').json())

@pytest.mark.security
def test_customer_cannot_use_admin_endpoint(client,customer):
    assert client.get('/api/admin/users',headers=customer['headers']).status_code==403

@pytest.mark.api
def test_missing_authentication(client): assert client.get('/api/bookings/me').status_code==401

@pytest.mark.api
def test_past_booking_rejected(client,customer):
    r=client.post('/api/bookings',headers=customer['headers'],json={'provider_id':1,'service_id':1,'appointment_time':(datetime.now()-timedelta(days=1)).isoformat()})
    assert r.status_code==422

@pytest.mark.regression
def test_booking_cancel_releases_slot(client,customer):
    slot=client.get('/api/providers/1/availability').json()[0]['start_time']
    payload={'provider_id':1,'service_id':1,'appointment_time':slot}
    made=client.post('/api/bookings',headers=customer['headers'],json=payload)
    assert made.status_code==201
    assert client.post('/api/bookings',headers=customer['headers'],json=payload).status_code==409
    assert client.delete(f"/api/bookings/{made.json()['id']}",headers=customer['headers']).status_code==204
    assert client.post('/api/bookings',headers=customer['headers'],json=payload).status_code==201

@pytest.mark.api
def test_invalid_resources_return_404(client,customer):
    future=(datetime.now()+timedelta(days=3)).isoformat()
    assert client.post('/api/bookings',headers=customer['headers'],json={'provider_id':999,'service_id':999,'appointment_time':future}).status_code==404

