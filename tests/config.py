from api.main import app
from api.schemas.user_schemas import UserCreate
from fastapi.testclient import TestClient

client = TestClient(app)

fake_users = [
    UserCreate(username="testuser1", password="password123"),
    UserCreate(username="testuser2", password="password123"),
    UserCreate(username="testuser3", password="password123"),
]
