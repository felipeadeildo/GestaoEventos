from app.api.main import api_router
from app.core.config import settings
from app.core.db import prisma
from app.core.security import get_password_hash
from app.models import Participant
from fastapi import FastAPI

app = FastAPI(
    title="Eventos",
)


app.include_router(api_router, prefix=settings.API_V1_STR)


async def startup():
    await prisma.connect()
    user = await Participant.prisma().find_unique(
        where={"email": settings.SUPERUSER_EMAIL}
    )
    if not user:
        await Participant.prisma().create(
            data={
                "email": settings.SUPERUSER_EMAIL,
                "password": get_password_hash(settings.SUPERUSER_PASSWORD),
                "name": "Admin",
            }
        )
        print("Superuser Created")
        print("Email: ", settings.SUPERUSER_EMAIL)
        print("Password: ", settings.SUPERUSER_PASSWORD)


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", prisma.disconnect)
