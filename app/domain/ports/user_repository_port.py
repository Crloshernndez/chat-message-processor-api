from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import User
from app.domain.value_objects import (
    EmailField,
    UsernameField
)


class UserRepositoryPort(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: EmailField) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_username(self, username: UsernameField) -> Optional[User]:
        pass