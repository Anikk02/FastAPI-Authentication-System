import logging

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
#from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.app.config import settings


logger = logging.getLogger(__name__)

DB_CONCURRENCY_LIMIT = 40
db_semaphore = asyncio.Semaphore(DB_CONCURRENCY_LIMIT)

try:
    engine_kwargs = {}

    #Convert DB Url to async
    '''DATABASE_URL = settings.DATABASE_URL.replace(
        'postgresql+psycopg2://','postgresql+asyncpg://'
    )'''

    if settings.DATABASE_URL.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}

    else:
        #increased app-side connection management from (size:5, 10 overflow) which was causing pool exhaustion + queueing
        #Also cuz default SQLAlchemy QueuePool configuration could not supply enough
        #DB connections, causing timeouts, internal server error and higher failure rate.
        engine_kwargs.update({
            'pool_size':50, #keep 50 persistent connections ready
            'max_overflow':100, #allow 100 extra temporary connection
            'pool_timeout':30, #wait up to 30s for a connection
            'pool_recycle':1800, #refresh older connections periodically
            'pool_pre_ping': True #prevents stale connections

        })
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo = False,
        **engine_kwargs
    )

    AsyncSessionLocal = sessionmaker(
        bind = engine,
        class_ = AsyncSession,
        expire_on_commit=False
    )

    Base = declarative_base()

    logger.debug("Async database engine and sessionmaker initialized successfully")

except SQLAlchemyError as e:
    logger.exception("Failed to initialize database engine")
    raise RuntimeError(f"Database initialization error: {e}") from e

except Exception as e:
    logger.exception("Unexpected error during database setup")
    raise RuntimeError(f"Unexpected database setup error: {e}") from e

async def safe_execute(db:AsyncSession, query):
    async with db_semaphore:
        return await db.execute(query)
    
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            logger.debug("Async database session opened")
            yield db
            await db.commit()
        
        except SQLAlchemyError as e:
            logger.exception("Database session error occurred")
            raise RuntimeError(f"Database session error: {e}") from e
    
        except Exception as e:
            logger.exception("Unexpected error during database session")
            await db.rollback()
            raise
    
        '''finally:
            logger.debug("Database session closed")
            await db.close()'''