from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRES_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        return pwd_context.verify(password, password_hash)

    def create_token(self, payload: dict) -> str:
        exp = datetime.utcnow() + timedelta(minutes=JWT_EXPIRES_MINUTES)
        data = {**payload, "exp": exp}
        return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

    def decode_token(self, token: str):
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
