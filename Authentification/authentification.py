import os

import fastapi.security
import jwt
from fastapi import HTTPException

from jwt import ExpiredSignatureError
from passlib.context import CryptContext

import settings
from DTO.user_authentification import User as UserAuth_DTO
from DTO.user import User as User_DTO
from services import user as UserServices
from errors.errors_raising import raise_400
from datetime import datetime, timedelta
import hashlib

from Authentification import emailUtils

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthHandler():

    def __init__(self, reset_tokens):
        self.reset_tokens = reset_tokens

    def encrypt_password(self, password: str):
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    def create_token(self, user: UserAuth_DTO):

        expiration_time = datetime.now() + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)

        data = {"sub": user.email,
                'password': user.password,
                'exp': int(expiration_time.timestamp())
                }

        encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return encoded_jwt

    def decode_token(self, token: str):

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

            return payload

        except ExpiredSignatureError as e:
            # custom_options = {
            #     "verify_exp": False,
            # }
            # payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM,
            #                      options=custom_options)
            raise_400('Your token has been expired')

        except Exception as e:
            raise raise_400("Invalid access token")

    def login_user(self, user: UserAuth_DTO, db):

        user_verified = UserServices.get_user(user.email, db)

        if not user_verified or not self.verify_password(user.password, user_verified.password):
            raise_400("Пользователя с такой почтой/паролем не существует")

        return self.create_token(user)

    def authentificate_user(self, access_token, db):

        payload = self.decode_token(access_token)

        email = payload.get("sub")
        password = payload.get("password")

        user = UserServices.get_user(email, db)

        if user is None or not self.verify_password(password, user.password):
            raise_400("You do not have access to this page!")

        return user

    async def generate_reset_token(self, email, db):
        user = UserServices.get_user(email, db)
        if not user:
            raise_400("пользователя с такой почтой в системе не существует")
            return

        hash_length = 32
        random_bytes = os.urandom(hash_length)

        hash_value = hashlib.sha256(random_bytes).hexdigest()
        await self.reset_tokens.set(hash_value, email)
        await self.reset_tokens.expire(hash_value, settings.CODE_EXPIRATION_TIME)

        emailUtils.reset_email.delay(hash_value, email)

        return True

    async def verify_reset_token(self, reset_token: str):
        data = await self.reset_tokens.get(reset_token)

        if not data:
            raise_400("Срок действия токена истек")

        return True

    async def reset_password(self, reset_token, new_password1, new_password2, db):
        data = await self.reset_tokens.get(reset_token)

        if not data:
            raise_400("Срок действия токена истек")

        if new_password1 != new_password2:
            raise_400("Пароли не совпадают")

        user = UserServices.change_password(data, self.encrypt_password(new_password1), db)
        if not user:
            raise_400("Пользователя с такой почтой не существует")

        await self.reset_tokens.delete(reset_token)
        return user

    def get_apikeyHeader(self, autoerror=True):
        return fastapi.security.APIKeyHeader(name="Authorization", auto_error=autoerror)



