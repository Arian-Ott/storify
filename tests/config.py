from api.main import app
from api.schemas.user_schemas import UserCreate
from fastapi.testclient import TestClient
from pydantic import BaseModel
import uuid


client = TestClient(app)

fake_users = [
    UserCreate(username="testuser1", password="password123"),
    UserCreate(username="testuser2", password="password123"),
    UserCreate(username="testuser3", password="password123"),
]


class UserCreate(BaseModel):
    username: str
    password: str


def generate_user(prefix="testuser"):
    uid = uuid.uuid4().hex[:6]
    return UserCreate(username=f"{prefix}_{uid}", password="secret123")
