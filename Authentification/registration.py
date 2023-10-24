import fastapi.security
import jwt
from fastapi import HTTPException

import random

from jwt import ExpiredSignatureError
from passlib.context import CryptContext

import settings
from DTO.user_registration import User as UserRegistration_DTO
from DTO.user import User as User_DTO
from DTO.user_confirmation import User as UserConfirmation_DTO
from services import user as UserServices
from errors.errors_raising import *
from passlib.context import CryptContext

from Authentification import emailUtils

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegistrationHandler:

    def encrypt_password(self, password: str):
        return pwd_context.hash(password)

    def register(self, user: UserRegistration_DTO, db):

        if UserServices.get_user(user.email, db):
            raise_400("User with this email already exist!")

        else:
            if user.password1 != user.password2:
                raise_400("Passwords do not match!")

            else:
                confirmation_code = random.randint(100000, 999999)

                sended = emailUtils.send_email(confirmation_code, user.email)

                if not sended:
                    raise_400(error)

                return {"status": 'Код успешно отправлен'}

    def confirm(self, user: UserConfirmation_DTO, db):
        pass