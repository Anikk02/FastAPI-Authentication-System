import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth import decode_access_token
from app.database import get_db
from app.models import User

logger = logging.getLogger(__name__)
security = HTTPBearer

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
)->User:
    try:
        token = credentials.credentials
        payload = decode_access_token(token)

        if payload is None:
            logger.warning("Authentication failed: invalid or expired token")
            raise HTTPException(
                status= 401,
                detail ="Invalid or expired token"
            )
        user_id = payload.get('user_id')
        if user_id is None:
            logger.warning("Authentication failed: user_id missing in token payload")
            raise HTTPException(
                status=401,
                detail="Invalid token payload"
            )
        user = db.query(User).filter(User.id==user_id).first()
        if user is None:
            logger.warning(f"Authentication failed: user not found for user_id={user_id}")
            raise HTTPException(
                status = 401,
                detail="User not found"
            )
        
        if not user.is_active:
            logger.warning("Authentication failed: inactive user user_id={user_id}")
            raise HTTPException(
                status=403,
                detail= "Inactive user accound"
            )
        
        logger.info(f"Authenticated user successfully: user_id={user_id}")
        return user
    except HTTPException:
        raise

    except Exception as e:
        logger.exception("Unexpected error while authenticating current user")
        raise HTTPException(
            status=501,
            detail = "Internal server error during authentication"
        ) from e