from passlib.context import CryptContext

crypto_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a password using Argon2.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    match password:
        case None | "":
            raise ValueError("Password must not be empty")
        case str() if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        case str() if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        case str() if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        case str() if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
    
    return crypto_context.hash(password)