from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from Authentification.authentification import AuthHandler
from Authentification.registration import RegistrationHandler

from DTO.user_registration import User as UserRegistration_DTO
from DTO.user import User as User_DTO
from DTO.user_authentification import User as UserAuth_DTO
from DTO.prompt import Prompt as Prompt_DTO

from models.model import get_db
import settings
import requests

from errors.errors_raising import raise_400

router = APIRouter()

Auth = AuthHandler()
Registr = RegistrationHandler()


@router.post("/register", status_code=200)
async def register(data: UserRegistration_DTO = None, db: Session = Depends(get_db)):
    user = Registr.register(data, db)
    return user


@router.post("/login", status_code=200)
async def login(data: UserAuth_DTO = None, db: Session = Depends(get_db)):
    token: str = Auth.login_user(user=data, db=db)
    return {"token": token}


@router.post("/get_image", status_code=200)
async def get_image(access_token: Annotated[str, Depends(Auth.get_apikeyHeader())], prompt: Prompt_DTO,
                    db: Session = Depends(get_db)):
    user = Auth.authentificate_user(access_token, db)

    links = ['https://s2.best-wallpaper.net/wallpaper/1680x1050/1808/Canada-Bow-Lake-pier_1680x1050.jpg',
             'https://laplaya-rus.ru/wp-content/uploads/2/0/c/20c206aa2a46b11c353982ffa54611bf.jpeg',
             'https://www.fonstola.ru/images/201511/fonstola.ru_210056.jpg']

    # response = requests.get(settings.API_LINK, params={"name" : "Amir"})
    #
    # if response.status_code == 200:
    #     return response.json()
    # else:
    #     raise_400("Something went wrong :(")

    return {"links": links}


