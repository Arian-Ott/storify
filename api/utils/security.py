from passlib.context import CryptContext


crypto_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password must not be empty")

    return crypto_context.hash(password)
