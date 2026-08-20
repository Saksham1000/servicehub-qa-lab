import pytest

@pytest.mark.graphql
def test_services_query(client):
    r=client.post('/graphql',json={'query':'{ services { id name category } }'})
    assert r.status_code==200 and len(r.json()['data']['services'])>=3

@pytest.mark.graphql
def test_query_variables_and_filter(client):
    q='query Find($term: String){ services(search:$term){ name } }'
    r=client.post('/graphql',json={'query':q,'variables':{'term':'mass'}})
    assert r.json()['data']['services'][0]['name']=='Massage'

@pytest.mark.graphql
def test_invalid_field_has_error(client):
    r=client.post('/graphql',json={'query':'{ services { unknownField } }'})
    assert r.status_code==200 and r.json().get('errors')

@pytest.mark.graphql
@pytest.mark.security
def test_protected_appointments_query(client):
    r=client.post('/graphql',json={'query':'{ appointments { id status } }'})
    assert r.json()['data'] is None and r.json()['errors']
