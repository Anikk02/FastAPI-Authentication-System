import logging

from fastapi import FastAPI

from app.database import Base, engine
from app.logger import setup_logging
from app import models
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router

setup_logging()
logger = logging.getLogger(__name__)

def create_application()->FastAPI:
    try:
        logger.info("Starting FastAPI application setup")

        app = FastAPI(
            title="FastAPI Auth System",
            description="A modular authentication system with JWT, logging, and protected routes",
            version='1.0.0'
        )

        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

        app.include_router(auth_router)
        app.include_router(user_router)
        logger.info("API routers registered successfully")

        @app.get('/')
        def root()->dict[str,str]:
            logger.info("Root endpoint accessed")
            return {'message': "FastAPI Auth System is running"}
        logger.info("FastAPI application setup completed successfully")
        return app
    
    except Exception as e:
        logger.exception("Failed to create FastAPI application")
        raise RuntimeError(f"Application startup failed: {e}") from e
    

app = create_application()
