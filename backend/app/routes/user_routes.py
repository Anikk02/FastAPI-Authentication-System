import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.models.user import User
from app.schemas import UserResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.get(
    '/me',
    response_model = UserResponse,
    status_code=200
)
async def read_current_user(
    current_user: User = Depends(get_current_user)
)->UserResponse:
    try:
        logger.info(f"/auth/me accessed by user_id={current_user.id}")
        return current_user
    
    except HTTPException:
        raise

    except Exception as e:
        logger.exception("Unexpected error while fetching current user")
        raise HTTPException(
            status_code = 500,
            detail = "Internal server error while fetching current user"
        ) from e
    