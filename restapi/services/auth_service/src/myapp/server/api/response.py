from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool
    message: str = ""
    data: T | None = None


def success_response(data: Any) -> APIResponse:
    return APIResponse(success=True, data=data)


def success_message_response(message: str, data: Any) -> APIResponse:
    return APIResponse(success=True, message=message, data=data)


def error_response(message: str) -> APIResponse:
    return APIResponse(success=False, message=message)


# ============================================================================
# Domain-specific response models
# ============================================================================

class UserResponse(BaseModel):
    username: str
    email: str
    password_changed_at: datetime | None = None
    created_at: datetime | None = None


class LoginUserResponse(BaseModel):
    session_id: str
    access_token: str
    access_token_expires_at: datetime
    refresh_token: str
    refresh_token_expires_at: datetime
    user: UserResponse


class RenewAccessTokenResponse(BaseModel):
    access_token: str
    access_token_expires_at: datetime
