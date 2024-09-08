from fastapi.responses import JSONResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from loguru import logger

from utils.settings import getSettings


settings = getSettings()
conf = ConnectionConfig(
    MAIL_USERNAME=settings.ADMIN_EMAIL_USERNAME,
    MAIL_PASSWORD=settings.ADMIN_EMAIL_PASSWORD,
    MAIL_FROM=settings.ADMIN_EMAIL,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
fm = FastMail(conf)

@logger.catch(message=f"email has not sent")
async def send_email(
        recipients: list[EmailStr],
        subject: str,
        body,
        subtype: MessageType = MessageType.html,
        *args,
        **kwargs
) -> None:
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=subtype
    )
    await fm.send_message(message)
    logger.debug(f"email has been sent for {recipients}")