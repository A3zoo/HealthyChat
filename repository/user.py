from uuid import UUID
from models.user import CreateUserModel, User, UserModel
from database import Session
from typing import Optional


def get_user(id: UUID) -> Optional[User]:
    with Session() as session:
        account = session.get(User, id)
        return account


def get_user_by_id(id: UUID) -> Optional[UserModel]:
    with Session() as session:
        user = session.query(User).filter(User.id == id).first()
        if user is None:
            return None
        return UserModel.model_validate(user)

def create_user(user: CreateUserModel) -> UserModel:
    with Session() as session:
        new_user = User(
            ip_address=user.ip_address,
            email=user.email,
            password=user.password,
        )
        session.add(new_user)
        session.commit()

        return UserModel.model_validate(user)


