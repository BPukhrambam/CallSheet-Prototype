import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_base_route():
    response = client.get("/")
    data = response.json()
    assert "projects" in data
    assert "user" in data
    assert "your_projects" in data
    assert response.json()["title"] == "Home"

def test_register_get():
    response = client.get("/register")
    data = response.json()
    assert "skills" in data
    assert response.json()["title"] == "Register"

def test_login_get():
    response = client.get("/login")
    data = response.json()
    assert response.json()["title"] == "Sign In"
