from tests.config import client
from tests.config import fake_users


PREFIX = "auth/"


def test_create_users():
    for user in fake_users:
        response = client.post(PREFIX + "users/", json=user.model_dump())
        assert response.status_code == 201, (
            f"Failed to create user {user.username}: {response.text}"
        )
        data = response.json()
        assert data["username"] == user.username, (
            f"Expected username {user.username}, got {data['username']}"
        )
        assert "id" in data, "Response should contain user ID"


def test_duplicate_user_creation():
    for user in fake_users:
        response = client.post(PREFIX + "users/", json=user.model_dump())
        assert response.status_code == 400, (
            f"Failed to create user {user.username}: {response.text}"
        )
        assert "Username already exists" in response.text, (
            f"Expected 'Username already exists' error for {user.username}, got {response.text}"
        )

def test_delete_user():
    # First create a user to delete
    for user in fake_users:
        jwt_token = client.post(
            "jwt/token", data={"username": user.username, "password": user.password}
        ).json().get("access_token")
        assert jwt_token, "JWT token should be created successfully"
        client.headers.update({"Authorization": f"Bearer {jwt_token}"})
        response = client.delete(PREFIX + "users/")
        assert response.status_code == 204, (
            f"Failed to delete user {user.username}: {response.text}"
        )