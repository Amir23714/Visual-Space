import random
from DTO.user_registration import User as UserRegistration_DTO
from DTO.user import User as User_DTO
from DTO.user_confirmation import User as UserConfirmation_DTO
from services import user as UserServices
from errors.errors_raising import *
from passlib.context import CryptContext

from Authentification import emailUtils
import json
import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegistrationHandler:

    def __init__(self, confirmation_codes):
        self.confirmation_codes = confirmation_codes

    def encrypt_password(self, password: str):
        return pwd_context.hash(password)

    def jsonDictionary(self, dictionary: dict) -> str:
        return json.dumps(dictionary)

    def dictJson(self, jsonDict: str) -> dict:
        return json.loads(jsonDict)

    async def register(self, user: UserRegistration_DTO, db):

        if UserServices.get_user(user.email, db):
            raise_400("Пользователь с такой почтой уже существует!")

        else:
            if user.password1 != user.password2:
                raise_400("Пароли не совпадают!")

            else:
                confirmation_code = random.randint(100000, 999999)

                sended = emailUtils.send_email.delay(confirmation_code, user.email)

                if not sended:
                    raise_400('Internal server error')
                else:
                    data = {
                        'email': user.email,
                        'password1': user.password1,
                        'password2': user.password2,
                        'username': user.username,
                        'confirmation_code': str(confirmation_code)
                    }

                    await self.confirmation_codes.set(user.email, self.jsonDictionary(data))
                    await self.confirmation_codes.expire(user.email, settings.CODE_EXPIRATION_TIME)

                    return {"status": 'Код успешно отправлен'}

    async def confirm(self, user: UserConfirmation_DTO, db):

        confirmation_code = str(user.confirmation_code)
        data = await self.confirmation_codes.get(user.email)

        if not data:
            raise_400("Ваш код подтверждения истек, зарегистрируйтесь заново")

        data = self.dictJson(data)

        initial_code = data['confirmation_code']

        if user.email != data['email'] or user.password1 != data['password1'] or user.password2 != data[
            'password2'] or user.username != data['username']:
            raise_400('Одно из полей не совпадает с тем, что вы ввели ранее. Регистрация отклонена')

        elif confirmation_code != initial_code:
            raise_400("Неверный код подтверждения")

        else:
            del user.confirmation_code
            try:
                await self.confirmation_codes.delete(user.email)
            except Exception as e:
                print(e)

            user.password1 = self.encrypt_password(user.password1)
            user = UserServices.create_user(user, db)

            return {"status": 'Вы успешно зарегистрировались!'}
