import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.domain.value_objects import (
    UUIDField,
    SenderField,
    ContentField,
    DatetimeField
)


@dataclass(frozen=True)
class Message:
    session_id: UUIDField
    content: ContentField
    timestamp: DatetimeField
    sender: SenderField
    character_count: Optional[int]
    word_count: Optional[int]
    processed_at: Optional[DatetimeField]

    id: Optional[UUIDField] = None
    created_at: Optional[DatetimeField] = None
    updated_at: Optional[DatetimeField] = None

    def __post_init__(self):
        if self.id is None:
            object.__setattr__(self, 'id', uuid.uuid4())
        if self.created_at is None:
            object.__setattr__(
                self,
                'created_at',
                DatetimeField(datetime.now())
                )
        if self.updated_at is None:
            object.__setattr__(
                self,
                'updated_at',
                DatetimeField(datetime.now())
                )

    @classmethod
    def create_from_dict(cls, data: dict) -> 'Message':
        return cls(
            id=data.get('id') or data.get('message_id'),
            session_id=data.get('session_id'),
            content=data.get('content'),
            timestamp=data.get('timestamp'),
            sender=data.get('sender'),
            word_count=data.get('word_count'),
            character_count=data.get('character_count'),
            processed_at=data.get('processed_at'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self) -> dict:
        metadata = {
            "word_count": self.word_count,
            "character_count": self.character_count,
            "processed_at": self.processed_at.value,
        }
        data = {
            "id": str(self.id),
            "session_id": str(self.session_id),
            "content": self.content.value,
            "timestamp": self.timestamp.value,
            "sender": self.sender.value,
            "metadata": metadata
        }

        return data
