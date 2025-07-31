from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from app.domain.entities import User as DomainUser
from app.domain.value_objects import (
    UUIDField,
    EmailField,
    UsernameField,
    PasswordHashField,
)
from app.domain.ports.user_repository_port import UserRepositoryPort
from app.infrastructure.persistence.orm_models import UserORM
from app.infrastructure.persistence.database import get_db
from app.infrastructure.decorators.exception_repository_handlers import (
    exception_repository_handlers
)


class SQLAlchemyUserRepository(UserRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    @exception_repository_handlers("crear usuario")
    def create_user(self, user: DomainUser) -> DomainUser:
        db_user = self._to_orm_model(user)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return self._to_domain_entity(db_user)

    @exception_repository_handlers("obtener usuario por username")
    def get_user_by_username(
            self,
            username: UsernameField
            ) -> Optional[DomainUser]:
        user_orm = self.db.query(UserORM).filter(
            UserORM.username == username.value
            ).first()

        return self._to_domain_entity(user_orm)

    @exception_repository_handlers("obtener usuario por email")
    def get_user_by_email(self, email: EmailField) -> Optional[DomainUser]:
        user_orm = self.db.query(UserORM).filter(
            UserORM.email == email.value
            ).first()

        return self._to_domain_entity(user_orm)

    def _to_domain_entity(self, user_orm: UserORM) -> DomainUser:
        if user_orm is None:
            return None
        return DomainUser(
            id=UUIDField(user_orm.id),
            email=EmailField(user_orm.email),
            username=UsernameField(user_orm.username),
            password_hash=PasswordHashField(user_orm.password),
            created_at=user_orm.created_at,
            updated_at=user_orm.updated_at
        )

    def _to_orm_model(self, user_entity: DomainUser) -> UserORM:
        return UserORM(
            id=str(user_entity.id),
            email=str(user_entity.email.value),
            username=str(user_entity.username),
            password=str(user_entity.password_hash),
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at
        )


def get_sqlalchemy_user_repository(
        db: Session = Depends(get_db)
        ) -> UserRepositoryPort:
    return SQLAlchemyUserRepository(db)
