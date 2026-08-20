import pytest
@pytest.mark.graphql
def test_live_graphql(api,base_url):
    r=api.post(base_url+'/graphql',json={'query':'{ providers { id name bio } }'})
    assert r.status_code==200 and isinstance(r.json()['data']['providers'],list)
