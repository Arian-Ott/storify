from passlib.context import CryptContext


crypto_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password must not be empty")

    return crypto_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not plain_password or not hashed_password:
        raise ValueError("Both plain password and hashed password must be provided")

    return crypto_context.verify(plain_password, hashed_password)
