from passlib.context import CryptContext

from gigtracker.schema.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(user: User | None, password: str) -> User | bool:
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return True
