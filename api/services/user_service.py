from api.models.user import UserModel
from api.db import get_db

def create_user(db, username, password):
    """
    Create a new user in the database.
    
    :param db: Database session
    :param username: Username of the user
    :param password_hash: Hashed password of the user
    :return: Created UserModel instance
    """
    if not username or not password:
        raise ValueError("Username and password must be provided")
    user = UserModel(username=username, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user