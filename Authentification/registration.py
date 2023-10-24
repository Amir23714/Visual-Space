import random
from DTO.user_registration import User as UserRegistration_DTO
from DTO.user import User as User_DTO
from DTO.user_confirmation import User as UserConfirmation_DTO
from services import user as UserServices
from errors.errors_raising import *
from passlib.context import CryptContext

from Authentification import emailUtils

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegistrationHandler:

    def __init__(self, confirmation_codes):
        self.confirmation_codes = confirmation_codes

    def encrypt_password(self, password: str):
        return pwd_context.hash(password)

    async def register(self, user: UserRegistration_DTO, db):

        if UserServices.get_user(user.email, db):
            raise_400("User with this email already exist!")

        else:
            if user.password1 != user.password2:
                raise_400("Passwords do not match!")

            else:
                confirmation_code = random.randint(100000, 999999)

                sended = emailUtils.send_email(confirmation_code, user.email)

                if not sended:
                    raise_400('Internal server error')
                else:
                    await self.confirmation_codes.set(user.email, str(confirmation_code))
                    return {"status": 'Код успешно отправлен'}

    async def confirm(self, user: UserConfirmation_DTO, db):

        confirmation_code = str(user.confirmation_code)
        if confirmation_code != await self.confirmation_codes.get(user.email):
            raise_400("Неверный код подтверждения")
        else:
            del user.confirmation_code
            try:
                await self.confirmation_codes.delete(user.email)
            except Exception as e:
                print(e)
            user = UserServices.create_user(user, db)

            return {"status": 'Вы успешно зарегистрировались!'}
