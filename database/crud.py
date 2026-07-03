from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Flashcard

async def get_user_by_id(session: AsyncSession, user_id: int) -> Flashcard | None:
    """Fetch a single user from the database by their Telegram ID."""
    result = await session.execute(select(Flashcard).where(Flashcard.id == user_id))
    return result.scalar_one_or_none()