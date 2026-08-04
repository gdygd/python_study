from datetime import datetime


class CreateUserParams:
    def __init__(
        self,
        username: str,
        hashed_password: str,
        full_name: str,
        email: str,
    ) -> None:
        self.username = username
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.email = email


class User:
    def __init__(
        self,
        username: str,
        hashed_password: str,
        full_name: str,
        email: str,
        password_changed_at: datetime | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self.username = username
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.email = email
        self.password_changed_at = password_changed_at
        self.created_at = created_at


class CreateSessionParams:
    def __init__(
        self,
        id: str,
        username: str,
        refresh_token: str,
        user_agent: str,
        client_ip: str,
        is_blocked: int,
        expires_at: datetime | None = None,
    ) -> None:
        self.id = id
        self.username = username
        self.refresh_token = refresh_token
        self.user_agent = user_agent
        self.client_ip = client_ip
        self.is_blocked = is_blocked
        self.expires_at = expires_at


class Session:
    def __init__(
        self,
        id: str,
        username: str,
        refresh_token: str,
        user_agent: str,
        client_ip: str,
        is_blocked: int,
        expires_at: datetime | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self.id = id
        self.username = username
        self.refresh_token = refresh_token
        self.user_agent = user_agent
        self.client_ip = client_ip
        self.is_blocked = is_blocked
        self.expires_at = expires_at
        self.created_at = created_at
