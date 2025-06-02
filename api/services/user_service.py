from api.models.user import UserModel
from api.db import get_db
from api.utils.security import hash_password
from uuid import UUID
from api.schemas.user_schemas import UserCreate


def create_user(user: UserCreate):
    """
    Create a new user in the database.

    :param db: Database session
    :param username: Username of the user
    :param password_hash: Hashed password of the user
    :return: Created UserModel instance
    """
    username = user.username
    password = user.password
    with get_db() as db:
        if not username or not password:
            raise ValueError("Username and password must be provided")
        if db.query(UserModel).filter(UserModel.username == username).first():
            raise ValueError("Username already exists")
        password_hash = hash_password(password)
        user = UserModel(username=username, password_hash=password_hash)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def get_user(user_id: str | UUID | None = None, username: str | None = None):
    with get_db() as db:
        if not user_id and not username:
            raise ValueError("Either user_id or username must be provided")
        return (
            db.query(UserModel)
            .filter(
                (UserModel.id == UUID(user_id))
                if user_id
                else (UserModel.username == username)
            )
            .first()
        )
