from typing import Optional

from app.core.security import verify_password
from app.models import Participant


async def authenticate(*, email: str, password: str) -> Optional[Participant]:
    db_user = await Participant.prisma().find_unique(where={"email": email})
    if not db_user:
        return None

    if not verify_password(password, db_user.password):
        return None

    return db_user
