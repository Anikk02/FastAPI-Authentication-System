import logging
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

logger = logging.getLogger(__name__)

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str)->str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Name cannot be empty or only spaces")
        return cleaned_value
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, value:str)->str:
        if value.strip()!=value:
            raise ValueError("Password cannot start or end with spaces")
        return value
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    role: str
    created_at: datetime

    model_config = {
        'from_attributes':True
    }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id:int | None = None

logger.info("Pydantic schemas loaded successfully")