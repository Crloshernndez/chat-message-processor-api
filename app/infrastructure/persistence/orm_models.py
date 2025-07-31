from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func
from .database import Base


class IdMixin:
    @declared_attr
    def id(cls):
        return Column(
            String,
            primary_key=True,
            index=True,
            nullable=False
        )


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime(timezone=True),
            onupdate=func.now(),
            server_default=func.now(),
            nullable=False
        )


class MessageORM(Base, IdMixin, TimestampMixin):
    __tablename__ = "messages"

    session_id = Column(
        String,
        index=True
    )
    content = Column(String)
    timestamp = Column(DateTime)
    sender = Column(String)
    word_count = Column(Integer)
    character_count = Column(Integer)
    processed_at = Column(DateTime)

    def __ref__(self):
        return f"<MessageORM(id='{self.id}', \
                session_id='{self.session_id}', \
                sender='{self.sender}')>"


class UserORM(Base, IdMixin, TimestampMixin):
    __tablename__ = "users"

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )
    username = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )
    password = Column(
        String,
        nullable=False
    )

    def __repr__(self):
        return f"<UserORM(id='{self.id}',\
            username='{self.username}',\
                email='{self.email}')>"
