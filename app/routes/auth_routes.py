import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.auth import create_access_token, hash_password, verify_password
from app.database import get_db
from app.models import User
from app.schemas import TokenResponse, UserLogin, UserRegister, UserResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/auth', tags=['Auth'])

def mask_email(email:str)->str:
    name, domain = email.split('@')
    if len(name)<=1:
        return f"@" + domain
    return f"{name[0]}***@" + domain

@router.post('/register', response_model=UserResponse, status_code=201)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
)->User:
    try:
        logger.info(f"Registration attempt: {mask_email(user_data.email)}")

        existing_user = db.query(User).filter(User.email==user_data.email).first()
        if existing_user:
            logger.warning(f"Registration failed: email already exists {mask_email(user_data.email)}")
            raise HTTPException(
                status_code=400,
                detail = "Email already registered"
            )
        
        new_user = User(
            name = user_data.name,
            email = user_data.email,
            hashed_password=hash_password(user_data.password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"User registered successfully: user_id={new_user.id}, email={mask_email(user_data.email)}")
        return new_user
    except HTTPException:
        raise

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Database error during user registration")
        raise HTTPException(
            status_code = 500,
            detail = "Database error during registration"
        ) from e
    except Exception as e:
        db.rollback()
        logger.exception("Unexpected error during user registration")
        raise HTTPException(
            status_code=500,
            detail = "Internal server error during registration"
        ) from e

@router.post('/login', response_model=TokenResponse, status_code=200)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db)
)->TokenResponse:
    try:
        logger.info(f"Login attempt for email={mask_email(user_data.email)}")

        user = db.query(User).filter(User.email == user_data.email).first()
        if user is None:
            logger.warning(f"Login failed: user not found for email={mask_email(user_data.email)}")
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )
        
        if not verify_password(user_data.password, user.hashed_password):
            logger.warning(f"Login failed: invalid password for email={mask_email(user_data.email)}")
            raise HTTPException(
                status_code=401,
                detail = "Invalid email or password"
            )
        
        if not user.is_active:
            logger.warning(f"Login denied: inactive user user_id={user.id}")
            raise HTTPException(
                status_code=403,
                detail = "Inactive user account"
            )
        
        access_token = create_access_token(data={'user_id':user.id})

        logger.info(f"User logged in successfully: user_id={user.id}")
        return TokenResponse(
            access_token=access_token,
            token_type='bearer'
        )
    except HTTPException:
        raise

    except SQLAlchemyError as e:
        logger.exception("Database error during user login")
        raise HTTPException(
            status_code=500,
            detail="Database error during login"
        )
    except Exception as e:
        logger.exception("Unexpected error during user login")
        raise HTTPException(
            status_code=500,
            detail = "Internal server error during login"
        ) from e
