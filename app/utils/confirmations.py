from flask import current_app
from flask_mail import Message
from app import mail
from app.logger import log


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
    )
    try:
        mail.send(msg)
    except ConnectionError as e:
        log(log.ERROR, "Connection error. Turn on your router: %s", e)
