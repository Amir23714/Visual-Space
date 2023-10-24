import datetime

from models.model import User as UserModel
from DTO.user_registration import User as UserRegistration_DTO


def create_user(data: UserRegistration_DTO, db):

    user = UserModel(username=data.username, password=data.password1, email=data.email, isAdmin=False)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

    except Exception as e:
        print(e)

    return user


def get_user(email : str, db):

    return db.query(UserModel).filter(UserModel.email == email).first()


