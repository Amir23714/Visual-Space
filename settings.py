from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", default="secret_key")
ALGORITHM = os.getenv("ALGORITHM", default="HS256")
API_LINK = os.getenv("API_LINK", default='https://api.agify.io?name=meelad')
ACCESS_TOKEN_EXPIRE_SECONDS = os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", default=30)

EMAIL_SENDER = os.getenv("EMAIL_SENDER", default="email_sender")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", default="email_password")