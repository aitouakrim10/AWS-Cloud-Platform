from sqlalchemy.orm import Session
from models.user import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str):
        return self.session.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()

    def create_user(self, username: str, email: str, password_hash: str):
        user = User(username=username, email=email, password_hash=password_hash)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
