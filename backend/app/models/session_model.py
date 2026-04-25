from sqlalchemy import ForeignKey, Boolean, Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database import Base
from datetime import datetime, timedelta

import logging

logger = logging.getLogger(__name__)

class Session(Base):
    __tablename__ = 'sessions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    refresh_token_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    device_info: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default = datetime.utcnow,
        nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    def __repr__(self)-> str:
        return f"Session(id={self.id}, user_id={self.user_id}, active={self.is_active})"
    
logger.info("Session model loaded successfully")
