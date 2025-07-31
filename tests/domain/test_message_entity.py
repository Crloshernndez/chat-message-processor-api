import uuid
from app.domain.entities.message import Message
from app.domain.value_objects import (
    UUIDField,
    SenderField,
    ContentField,
    DatetimeField
)


class TestMessageEntity:
    def test_message_creation_with_all_valid_data(
        self,
        valid_uuid_str,
        valid_datetime_now,
        valid_content_str
    ):
        message = Message(
            session_id=UUIDField(valid_uuid_str),
            content=ContentField(valid_content_str),
            timestamp=DatetimeField(valid_datetime_now),
            sender=SenderField("user"),
            word_count=5,
            character_count=28,
            processed_at=DatetimeField(valid_datetime_now)
        )

        assert isinstance(message.id, uuid.UUID)
        assert message.content.value == valid_content_str
        assert message.timestamp.value == valid_datetime_now
        assert message.sender.value == "user"
        assert message.word_count == 5
        assert message.character_count == 28

    def test_create_from_dict_with_all_valid_data(
            self,
            valid_uuid_str,
            valid_content_str,
            valid_datetime_now,
            ):
        """create a Message object from a valid dictionary."""
        message_data_str = {
            "id": UUIDField(valid_uuid_str),
            "session_id": UUIDField(valid_uuid_str),
            "content": ContentField(valid_content_str),
            "timestamp": DatetimeField(valid_datetime_now),
            "sender": SenderField("user"),
            "word_count": 5,
            "character_count": 28,
            "processed_at": DatetimeField(valid_datetime_now)
        }

        message = Message.create_from_dict(message_data_str)

        assert isinstance(message.id, UUIDField)
        assert isinstance(message.session_id, UUIDField)
        assert isinstance(message.content, ContentField)
        assert isinstance(message.timestamp, DatetimeField)
        assert isinstance(message.sender, SenderField)
        assert isinstance(message.processed_at, DatetimeField)

        assert str(message.id.value) == valid_uuid_str
        assert message.content.value == valid_content_str

    def test_create_from_dict_with_minimal_data(
            self,
            valid_uuid_str,
            valid_datetime_now
            ):
        """Create a Message object from a dictionary with minimal data."""
        message_data = {
            "session_id": UUIDField(valid_uuid_str),
            "content": ContentField("Minimal message."),
            "timestamp": DatetimeField(valid_datetime_now),
            "sender": SenderField("system")
        }

        message = Message.create_from_dict(message_data)

        assert isinstance(message.id, uuid.UUID)
        assert isinstance(message.session_id, UUIDField)
        assert isinstance(message.content, ContentField)
        assert isinstance(message.timestamp, DatetimeField)
        assert isinstance(message.sender, SenderField)
