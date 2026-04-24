import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ ADD THIS

from app.database import Base, engine
from app.logger import setup_logging
from app.models import user, session_model
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.redis_routes import router as redis_router

setup_logging()
logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    try:
        logger.info("Starting FastAPI application setup")

        app = FastAPI(
            title="FastAPI Auth System",
            description="A modular authentication system with JWT, logging, and protected routes",
            version='1.0.1'
        )

        # CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],  # frontend URL
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Async DB initialization
        @app.on_event('startup')
        async def on_startup():
            try:
                logger.info("Initializing database (async)")
                async with engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                logger.info("Database tables created successfully")
            except Exception as e:
                logger.exception("Database initialization failed")
                raise RuntimeError(f"Database initialization error: {e}") from e

        app.include_router(auth_router)
        app.include_router(user_router)
        app.include_router(redis_router)
        logger.info("API routers registered successfully")

        @app.get('/')
        async def root() -> dict[str, str]:
            logger.info("Root endpoint accessed")
            return {'message': "FastAPI Auth System is running"}

        logger.info("FastAPI application setup completed successfully")
        return app

    except Exception as e:
        logger.exception("Failed to create FastAPI application")
        raise RuntimeError(f"Application startup failed: {e}") from e


app = create_application()