from pydantic import BaseModel


class ResetPassword(BaseModel):
    reset_token: str

    password1: str

    password2: str
