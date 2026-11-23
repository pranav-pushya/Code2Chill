import os
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import dotenv_values
from fastapi import HTTPException

from .database import ENV_FILE


def mail_settings():
    return {**dotenv_values(ENV_FILE), **os.environ}


def mail_ready():
    settings = mail_settings()
    return bool(settings.get("RECRUITMENT_SMTP_HOST") and settings.get("RECRUITMENT_MAIL_FROM"))


def send_code(address: str, code: str):
    settings = mail_settings()
    message = EmailMessage()
    message["Subject"] = "Your Code2Chill application code"
    message["From"] = settings["RECRUITMENT_MAIL_FROM"]
    message["To"] = address
    message.set_content(
        f"Enter {code} on the Code2Chill application page to verify this email address. "
        "The code expires in 15 minutes. If you did not request it, you can ignore this email."
    )
    try:
        with smtplib.SMTP_SSL(
            settings["RECRUITMENT_SMTP_HOST"],
            int(settings.get("RECRUITMENT_SMTP_PORT") or 465),
            context=ssl.create_default_context(),
            timeout=8,
        ) as smtp:
            if settings.get("RECRUITMENT_SMTP_USER"):
                smtp.login(
                    settings["RECRUITMENT_SMTP_USER"], settings.get("RECRUITMENT_SMTP_PASSWORD", "")
                )
            smtp.send_message(message)
    except (OSError, ValueError, smtplib.SMTPException):
        raise HTTPException(503, "Couldn’t send the email. Try again in a minute.") from None
