from pydantic import BaseModel


class ResetToken(BaseModel):
    reset_token : str
