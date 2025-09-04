from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

# --- Base Schemas ---

class UserBase(BaseModel):
    """Base schema for user, contains shared fields."""
    email: EmailStr = Field(..., description="User's email address, must be unique.")
    username: str = Field(..., min_length=3, max_length=50, description="Unique username.")
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    user_id: str = Field(..., description="Employee ID or unique user identifier.")
    is_active: bool = True
    role: str = Field("admin", description="User role (e.g., 'admin', 'superadmin')")

    class Config:
        from_attributes = True

# --- Schemas for Creating Users ---

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, description="User's password.")
    confirm_password: str = Field(..., description="Password confirmation.")

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

# --- Schemas for Updating Users ---

class UserUpdate(BaseModel):
    """Schema for updating an existing user. All fields are optional."""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    role: Optional[str] = None

# --- Schemas for Database and Public Representation ---

class UserInDBBase(UserBase):
    """Schema for user data as stored in the database."""
    id: int
    public_id: str

class User(UserInDBBase):
    """Default user schema for API responses."""
    pass

class UserInDB(UserInDBBase):
    """Full user schema including the hashed password."""
    password_hash: str


# --- Schemas for Authentication ---

class Token(BaseModel):
    """Schema for the JWT access token."""
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """Schema for the data encoded in the JWT."""
    sub: Optional[str] = None  # 'sub' is standard for subject, here we use username
