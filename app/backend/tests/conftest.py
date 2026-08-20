import os,sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

BACKEND=Path(__file__).parents[1]
sys.path.insert(0,str(BACKEND))
os.environ["DATABASE_URL"]="sqlite:///./test_servicehub.db"
from app.database import Base,engine
from app.main import app

@pytest.fixture(scope="session")
def client():
    Base.metadata.drop_all(engine)
    with TestClient(app) as c: yield c
    Base.metadata.drop_all(engine)

@pytest.fixture
def customer(client):
    email=f"qa{os.urandom(4).hex()}@example.com"
    data={'name':'QA Customer','email':email,'password':'Strong123!'}
    created=client.post('/api/auth/register',json=data)
    assert created.status_code==201 and 'access_token' not in created.json()
    login=client.post('/api/auth/login',json={'email':email,'password':data['password']})
    return {'headers':{'Authorization':f"Bearer {login.json()['access_token']}"},'email':email}

@pytest.fixture
def admin(client):
    r=client.post('/api/auth/login',json={'email':'admin@servicehub.example','password':'Admin123!'})
    return {'Authorization':f"Bearer {r.json()['access_token']}"}


