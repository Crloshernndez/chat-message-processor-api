from typing import List, Tuple, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from app.domain.entities.message import Message as DomainMessage
from app.domain.ports.message_repository_port import MessageRepositoryPort
from app.domain.value_objects import (
    UUIDField,
    SenderField,
    ContentField,
    DatetimeField
)
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.orm_models import MessageORM
from app.infrastructure.decorators.exception_repository_handlers import (
    exception_repository_handlers
)


class SQLAlchemyMessageRepository(MessageRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    @exception_repository_handlers("crear mensaje")
    def create_message(self, message: DomainMessage) -> DomainMessage:
        db_message = self._to_orm_model(message)
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)

        return message

    @exception_repository_handlers("obtener mensaje por Id")
    def get_message_by_id(self, message_id: UUIDField) -> DomainMessage:
        message_orm = self.db.query(MessageORM).filter(
            MessageORM.id == str(message_id)
            ).first()

        return self._to_domain_entity(message_orm)

    @exception_repository_handlers("obtener mensajes por session")
    def get_message_by_session_id(
            self,
            session_id: UUIDField,
            limit: int = 50,
            offset: int = 0,
            sender: Optional[str] = None
            ) -> Tuple[List[DomainMessage], int]:

        base_query = self.db.query(MessageORM).filter(
            MessageORM.session_id == str(session_id)
        )

        if sender:
            base_query = base_query.filter(MessageORM.sender == sender)

        total_count = base_query.count()

        message_orm_list = (
            base_query
            .order_by(MessageORM.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        messages = (
            [self._to_domain_entity(message) for message in message_orm_list]
        )

        return messages, total_count

    def _to_orm_model(self, message_entity: DomainMessage) -> MessageORM:
        return MessageORM(
            id=str(message_entity.id.value),
            session_id=str(message_entity.session_id.value),
            content=message_entity.content.value,
            timestamp=message_entity.timestamp.value,
            sender=message_entity.sender.value,
            word_count=message_entity.word_count,
            character_count=message_entity.character_count,
            processed_at=message_entity.processed_at.value,
            created_at=message_entity.created_at.value,
            updated_at=message_entity.updated_at.value,
        )

    def _to_domain_entity(self, message_orm: MessageORM) -> DomainMessage:
        if message_orm is None:
            return None

        return DomainMessage(
            id=UUIDField(message_orm.id),
            session_id=UUIDField(message_orm.session_id),
            content=ContentField(message_orm.content),
            timestamp=DatetimeField(message_orm.timestamp),
            sender=SenderField(message_orm.sender),
            word_count=message_orm.word_count,
            character_count=message_orm.character_count,
            processed_at=DatetimeField(message_orm.processed_at),
            created_at=DatetimeField(message_orm.created_at),
            updated_at=DatetimeField(message_orm.updated_at),
        )


def get_sqlalchemy_message_repository(
        db: Session = Depends(get_db)
        ) -> MessageRepositoryPort:
    return SQLAlchemyMessageRepository(db)
