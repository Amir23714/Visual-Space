import smtplib
import settings
from email.mime.text import MIMEText
from email.header import Header


def send_email(confirmation_code: str | int, subject: str):
    sender = settings.EMAIL_SENDER
    password = settings.EMAIL_PASSWORD

    message = f"Ваша регистрация практически заверщена! Осталось совсем немного\n\n<h2>Ваш код подтверждения:<h2> <h1>{confirmation_code}<h1>"

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

