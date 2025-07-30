import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.domain.value_objects import (
    UUIDField,
    EmailField,
    PasswordField
)


@dataclass(frozen=True)
class User:
    email: EmailField
    username: str
    password_hash: PasswordField

    id: Optional[UUIDField] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.id is None:
            object.__setattr__(self, 'id', uuid.uuid4())
        if self.created_at is None:
            object.__setattr__(self, 'created_at', datetime.now())
        if self.updated_at is None:
            object.__setattr__(self, 'updated_at', datetime.now())

    @classmethod
    def create_from_dict(cls, data: dict) -> 'User':
        return cls(
            id=data.get('id'),
            email=data.get('email'),
            username=data.get('username'),
            password_hash=data.get('password_hash'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
