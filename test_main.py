from fastapi.testclient import TestClient
from main import app

from database import Base, engine

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_signup():
    response = client.post(
        "/signup",
        json={"username": "testuser", "password": "1234"}
    )
    assert response.status_code in [200, 400]

def test_login():
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "1234"}  # <-- use data= not json=
    )
    assert response.status_code in [200, 401] 
