import logging
from datetime import datetime, timezone

from sqlalchemy import Boolean, Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database import Base 

logger = logging.getLogger(__name__)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable = False)
    role: Mapped[str] = mapped_column(String(50), default='user', nullable = False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default = lambda: datetime.now(timezone.utc),
        nullable = False
    )

    def __repr__(self)->str:
        return f"User(id={self.id}, email='{self.email}', role='{self.role}')"
    
    logger.info("User model loaded successfully")