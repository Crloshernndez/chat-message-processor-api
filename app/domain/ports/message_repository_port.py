from abc import ABC, abstractmethod
from app.domain.entities import Message
from app.domain.value_objects import (
    UUIDField
)


class MessageRepositoryPort(ABC):
    @abstractmethod
    def create_message(self, message: Message) -> Message:
        pass

    @abstractmethod
    def get_message_by_id(self, id: UUIDField) -> Message:
        pass

    @abstractmethod
    def get_message_by_session_id(self, id: UUIDField) -> Message:
        pass
