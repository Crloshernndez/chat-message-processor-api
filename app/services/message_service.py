from datetime import datetime
from typing import Optional, List, Tuple
from fastapi import Depends
from app.domain.ports.message_repository_port import MessageRepositoryPort
from app.domain.entities import Message
from app.domain.exceptions import (
    DomainValidationException
)
from app.domain.value_objects import (
    UUIDField,
    SenderField,
    ContentField,
    DatetimeField
)
from app.infrastructure.persistence.repositories.message_repository import (
    get_sqlalchemy_message_repository
)


class MessageService:
    def __init__(self, message_repository: MessageRepositoryPort):
        self._message_repository = message_repository

    def register_message(
            self,
            message_data: dict
            ) -> Message:

        new_message_entity = self._validate_message_data(message_data)

        if self._message_repository.get_message_by_id(new_message_entity.id):
            raise DomainValidationException(
                message="Mensaje con id registrado",
                detail="Ya existe un mensaje con el id."
            )

        created_message = self._message_repository.create_message(
            new_message_entity
            )
        return created_message

    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        message_uuid_field = UUIDField(message_id)
        return self._message_repository.get_message_by_id(message_uuid_field)

    def get_message_by_session_id(
            self,
            session_id: str,
            limit: int = 50,
            offset: int = 0,
            sender: Optional[str] = None
            ) -> Tuple[List[Message], int]:
        session_uuid_field = UUIDField(session_id)
        return self._message_repository.get_message_by_session_id(
            session_uuid_field,
            limit=limit,
            offset=offset,
            sender=sender
            )

    def _validate_message_data(self, message_data: dict) -> Message:
        content = ContentField(message_data.get('content'))
        character_count = self._calculate_character_count(content.value)
        word_count = self._calculate_word_count(content.value)

        return Message.create_from_dict({
            'id': UUIDField(message_data.get('message_id')),
            'session_id': UUIDField(message_data.get('session_id')),
            'content': content,
            'timestamp': DatetimeField(message_data.get('timestamp')),
            'sender': SenderField(message_data.get('sender')),
            'word_count': word_count,
            'character_count': character_count,
            'processed_at': DatetimeField(datetime.now())
        })

    def _calculate_character_count(self, content: ContentField) -> int:
        return len(content.replace(' ', '')) if content else 0

    def _calculate_word_count(self, content: ContentField) -> int:
        if not content or not content.strip():
            return 0
        return len(content.strip().split())


def get_message_service(
        message_repository: MessageRepositoryPort = Depends(
            get_sqlalchemy_message_repository
            )
        ) -> 'MessageService':
    return MessageService(message_repository)
