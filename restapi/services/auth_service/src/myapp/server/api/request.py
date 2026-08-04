from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    username: str = Field(..., pattern=r"^[a-zA-Z0-9]+$")
    password: str = Field(..., min_length=4)
    full_name: str
    email: EmailStr


class LoginUserRequest(BaseModel):
    username: str = Field(..., pattern=r"^[a-zA-Z0-9]+$")
    password: str = Field(..., min_length=4)


class RenewAccessTokenRequest(BaseModel):
    refresh_token: str


class LogoutUserRequest(BaseModel):
    refresh_token: str
