from fastapi import HTTPException


def raise_400(message: str):
    raise HTTPException(status_code=400, detail=message)
