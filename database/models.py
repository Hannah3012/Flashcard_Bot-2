from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from session import Base


class Flashcard(Base): #inherits from the Base class so sqlalchemy knows this class represents a database table
    __tablename__ = "Flashcards"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    front: Mapped[str] = mapped_column(nullable=False)
    back: Mapped[str] = mapped_column(nullable=True)
    joined_at: Mapped[datetime] = mapped_column(server_default=func.now())


