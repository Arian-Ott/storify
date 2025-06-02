from tests.config import client
import pytest

PREFIX = "auth/"


@pytest.fixture
def create_user():
    def _create(user):
        response = client.post(PREFIX + "users/", json=user.model_dump())
        return response

    return _create


@pytest.fixture
def delete_user():
    def _delete(user):
        jwt_token = (
            client.post(
                "jwt/token", data={"username": user.username, "password": user.password}
            )
            .json()
            .get("access_token")
        )
        assert jwt_token, "JWT token should be created successfully"
        client.headers.update({"Authorization": f"Bearer {jwt_token}"})
        return client.delete(PREFIX + "users/")

    return _delete
