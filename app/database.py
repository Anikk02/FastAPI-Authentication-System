import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


logger = logging.getLogger(__name__)

try:
    engine_kwargs = {}

    if settings.DATABASE_URL.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}

    engine = create_engine(
        settings.DATABASE_URL,
        **engine_kwargs
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    Base = declarative_base()

    logger.info("Database engine and sessionmaker initialized successfully")

except SQLAlchemyError as e:
    logger.exception("Failed to initialize database engine")
    raise RuntimeError(f"Database initialization error: {e}") from e

except Exception as e:
    logger.exception("Unexpected error during database setup")
    raise RuntimeError(f"Unexpected database setup error: {e}") from e


def get_db():
    db = SessionLocal()
    try:
        logger.info("Database session opened")
        yield db
        
    except SQLAlchemyError as e:
        logger.exception("Database session error occurred")
        raise RuntimeError(f"Database session error: {e}") from e
    
    except Exception as e:
        logger.exception("Unexpected error during database session")
        raise RuntimeError(f"Unexpected database session error: {e}") from e
    
    finally:
        db.close()
        logger.info("Database session closed")