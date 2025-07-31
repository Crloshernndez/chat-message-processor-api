import uuid
import pytest
from app.domain.entities.message import Message
from app.domain.value_objects import UUIDField
from app.domain.exceptions import (
    DomainValidationException
)


class TestMessageService:
    def test_register_message_successfully(
            self,
            message_service,
            message_repository_mock,
            valid_message_data,
            mocked_message_entity
    ):
        """
        message successfully when the data is valid
        and the message ID does not exist.
        """

        message_repository_mock.get_message_by_id.return_value = None
        message_repository_mock.create_message.return_value = (
            mocked_message_entity
        )

        registered_message = message_service.register_message(
            valid_message_data
            )

        message_repository_mock.get_message_by_id.assert_called_once()
        message_repository_mock.create_message.assert_called_once()
        assert isinstance(registered_message, Message)
        assert registered_message.content.value == (
            valid_message_data['content']
        )

        assert registered_message.word_count == 5
        assert registered_message.character_count == 26

    def test_register_message_raises_exception_if_message_exists(
            self,
            message_service,
            message_repository_mock,
            valid_message_data,
            mocked_message_entity
            ):
        """
        Throw Domain ValidationException if a message with the
        same ID already exists.
        """

        message_repository_mock.get_message_by_id.return_value = (
            mocked_message_entity
        )

        with pytest.raises(DomainValidationException) as exc_info:
            message_service.register_message(valid_message_data)

        assert "Mensaje con id registrado" in str(exc_info.value.message)
        message_repository_mock.get_message_by_id.assert_called_once()
        message_repository_mock.create_message.assert_not_called()

    def test_get_message_by_id_successfully(
        self,
        message_service,
        message_repository_mock,
        mocked_message_entity
    ):
        """
        retrieve a message by its ID when the ID is valid and exists.
        """
        message_repository_mock.get_message_by_id.return_value = (
            mocked_message_entity
        )

        retrieved_message = message_service.get_message_by_id(
            str(mocked_message_entity.id.value)
            )

        message_repository_mock.get_message_by_id.assert_called_once_with(
            mocked_message_entity.id
            )
        assert retrieved_message == mocked_message_entity

    def test_get_message_by_id_returns_none_if_not_found(
            self,
            message_service,
            message_repository_mock
            ):
        """
        Return None if a message with the given ID is not found.
        """
        message_id_str = str(uuid.uuid4())
        message_repository_mock.get_message_by_id.return_value = None

        retrieved_message = message_service.get_message_by_id(message_id_str)

        message_repository_mock.get_message_by_id.assert_called_once_with(
            UUIDField(message_id_str)
            )
        assert retrieved_message is None

    @pytest.mark.parametrize("content, expected_words, expected_chars", [
        ("Este es un mensaje.", 4, 16),
        ("  Hola mundo  ", 2, 9),
        ("Uno.", 1, 4),
        ("", 0, 0),
        ("    ", 0, 0),
        (None, 0, 0)
    ])
    def test_calculate_counts_correctly(
            self,
            message_service,
            content,
            expected_words,
            expected_chars
            ):
        """
        Verify that the private word and character count methods
        work for various test cases.
        """
        word_count = message_service._calculate_word_count(content)
        char_count = message_service._calculate_character_count(content)

        assert word_count == expected_words
        assert char_count == expected_chars
