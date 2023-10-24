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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthHandler():

    def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    def get_token(self, user: UserAuth_DTO):

        expiration_time = datetime.utcnow() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)

        data = {"sub": user.email,
                'password': user.password
                }

        encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return encoded_jwt

    def decode_token(self, token: str):

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

            return payload

        except Exception as e:
            raise raise_400("Invalid access token")

    def login_user(self, user: UserAuth_DTO, db):

        user_verified = UserServices.get_user(user.email, db)

        if not user_verified or not self.verify_password(user.password, user_verified.password):
            raise_400("User with such email/password do not exist")

        return self.get_token(user)

    def authentificate_user(self, access_token, db):

        payload = self.decode_token(access_token)

        email = payload.get("sub")
        password = payload.get("password")

        user = UserServices.get_user(email, db)

        if user is None:
            raise_400("You do not have access to this page!")

        return user

    def get_apikeyHeader(self, autoerror=True):
        return fastapi.security.APIKeyHeader(name="Authorization", auto_error=autoerror)

# if __name__ == "__main__":
#     print(datetime.utcnow() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS))
