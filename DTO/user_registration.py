from pydantic import BaseModel


class User(BaseModel):
    email: str

    password1: str

    password2: str

    username: str

