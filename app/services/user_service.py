from app.domain.entities import User
from app.domain.ports.user_repository_port import UserRepositoryPort
from app.infrastructure.persistence.repositories.user_repository import (
    get_sqlalchemy_user_repository
)
from app.domain.value_objects import (
    UUIDField,
    EmailField,
    UsernameField,
    PasswordRawField,
    PasswordHashField
)

from app.domain.exceptions import (
    DomainValidationException
)
from fastapi import Depends
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, user_repository: UserRepositoryPort):
        self._user_repository = user_repository

    def register_user(
            self,
            user_data: dict
            ) -> User:
        password = PasswordRawField(user_data.get('password'))
        email = EmailField(user_data.get('email'))
        username = UsernameField(user_data.get('username'))

        if self._user_repository.get_user_by_email(email):
            raise DomainValidationException(
                message="Usuario ya se encuentra registrado",
                detail=f"Ya existe un usuario con el email '{email}'.",
                code="USER_ALREADY_REGISTERED"
            )
        if self._user_repository.get_user_by_username(username):
            raise DomainValidationException(
                message="Usuario ya se encuentra registrado",
                detail=f"Ya existe un usuario con el nombre de\
                    usuario '{username}'.",
                code="USER_ALREADY_REGISTERED"
            )

        hashed_password = PasswordHashField(
            self._get_password_hash(password.value)
        )

        new_user_entity = User(
            id=UUIDField(uuid.uuid4()),
            email=email,
            username=username,
            password_hash=hashed_password
        )

        created_user = self._user_repository.create_user(new_user_entity)
        return created_user

    def authenticate_user(self, user_credentials: dict) -> User:
        email = EmailField(user_credentials.get('email'))
        password = PasswordRawField(user_credentials.get('password'))

        user = self._user_repository.get_user_by_email(email)
        if not user:
            raise DomainValidationException(
                message="Credenciales incorrectas.",
                detail="Se ingresaron credenciales incorrectas",
                code="INVALID_CREDENTIALS"
            )
        if not self._verify_password(
            password.value,
            user.password_hash.value
        ):
            raise DomainValidationException(
                message="Credenciales incorrectas.",
                detail="Se ingresaron credenciales incorrectas",
                code="INVALID_CREDENTIALS"
            )

        return user

    def _get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def _verify_password(
            self,
            plain_password: str,
            hashed_password: str
            ) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


def get_user_service(
        user_repository: UserRepositoryPort = Depends(
            get_sqlalchemy_user_repository
            )
        ) -> 'UserService':
    return UserService(user_repository)
