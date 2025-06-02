from api.models.user import UserModel
from api.db import get_db
from api.utils.security import hash_password
from uuid import UUID
from api.schemas.user_schemas import UserCreate
from sqlalchemy.orm import load_only

def create_user(user: UserCreate):
    username = user.username
    password = user.password
    with next(get_db()) as db:
        if not username or not password:
            raise ValueError("Username and password must be provided")
        if db.query(UserModel).filter(UserModel.username == username).first():
            raise ValueError("Username already exists")
        password_hash = hash_password(password)
        new_user = UserModel(username=username, password=password_hash)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


def get_user(user_id: str | UUID | None = None, username: str | None = None):
    with next(get_db()) as db:
        if not user_id and not username:
            raise ValueError("Either user_id or username must be provided")

        query = db.query(UserModel).filter(UserModel.username == username) if username else db.query(UserModel).filter(UserModel.id == user_id)
        
        user = query.first()
    return user
def delete_user(user_id: str | UUID):
    with next(get_db()) as db:
        if isinstance(user_id, str):
            user_id = UUID(user_id)
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        db.delete(user)
        db.commit()