import smtplib
import settings
from email.mime.text import MIMEText
from email.header import Header
from typing import Union
from celery import Celery

sender = settings.EMAIL_SENDER
password = settings.EMAIL_PASSWORD

celery = Celery("emails", broker="redis://localhost:6379/2")


@celery.task
def send_email(confirmation_code: Union[str, int], subject: str):
    message = f"Ваша регистрация практически завершена! Осталось совсем немного\n\n<h2>Ваш код подтверждения:<h2> <h1>{confirmation_code}<h1>"

    msg = MIMEText(message, 'html', 'utf-8')
    msg['Subject'] = Header('Код подтверждения Visual Space', 'utf-8')
    msg['From'] = sender
    msg['To'] = subject

    server = smtplib.SMTP('smtp.yandex.ru', 587, timeout=20)

    try:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, subject, msg.as_string())

        return True

    except Exception as e:
        return False

    finally:
        server.quit()


@celery.task
def reset_email(token: str, subject: str):
    message = f"Ссылка для восстановления пароля<br><br><h2>Перейдите по ссылке<h2> <a>file:///home/amir/projects/JSprojects/Visual-Space-JS/templates/reset.html?reset_token={token}<a>"

    msg = MIMEText(message, 'html', 'utf-8')
    msg['Subject'] = Header('Восстановление пароля Visual Space', 'utf-8')
    msg['From'] = sender
    msg['To'] = subject

    server = smtplib.SMTP('smtp.yandex.ru', 587, timeout=20)

    try:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, subject, msg.as_string())

        return True

    except Exception as e:
        return False

    finally:
        server.quit()
