from datetime import datetime
import uuid
import pytest
from unittest.mock import create_autospec, MagicMock
from app.services.user_service import UserService
from app.services.message_service import MessageService
from app.domain.ports.user_repository_port import UserRepositoryPort
from app.domain.ports.message_repository_port import MessageRepositoryPort
from app.domain.entities.user import User
from app.domain.entities.message import Message
from app.domain.value_objects import (
    UUIDField,
    EmailField,
    SenderField,
    ContentField,
    UsernameField,
    DatetimeField,
    PasswordHashField
)


@pytest.fixture
def valid_uuid_str():
    return str(uuid.uuid4())


@pytest.fixture
def valid_email_str():
    return "test@example.com"


@pytest.fixture
def valid_username_str():
    return "testuser123"


@pytest.fixture
def valid_password_raw_str():
    return "A123456z"


@pytest.fixture
def valid_password_hash_str():
    return "$2b$12$d1.KSoZmbtgRKbbFO8uY1.vRcbZDV0DBzrXIP/v/Cy8MBo7xlf/OS"


@pytest.fixture
def valid_content_str():
    return "Este es un mensaje completamente válido."


@pytest.fixture
def content_with_inappropriate_words():
    return "Este es un mensaje malo y ofensivo."


@pytest.fixture
def valid_datetime_now():
    return datetime.now()


@pytest.fixture
def user_repository_mock():
    return create_autospec(UserRepositoryPort)


@pytest.fixture
def user_service(user_repository_mock):
    return UserService(user_repository_mock)


@pytest.fixture
def valid_user_data():
    return {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "StrongPassword123"
    }


@pytest.fixture
def mocked_user_entity(valid_user_data, user_service):
    hashed_password = user_service._get_password_hash(
        valid_user_data["password"]
        )
    return User(
        id=UUIDField(uuid.uuid4()),
        email=EmailField(valid_user_data["email"]),
        username=UsernameField(valid_user_data["username"]),
        password_hash=PasswordHashField(hashed_password)
    )


@pytest.fixture
def message_repository_mock():
    return create_autospec(MessageRepositoryPort)


@pytest.fixture
def message_service(message_repository_mock):
    return MessageService(message_repository_mock)


@pytest.fixture
def valid_message_data():
    return {
        "message_id": str(uuid.uuid4()),
        "session_id": str(uuid.uuid4()),
        "content": "Este es un mensaje de prueba.",
        "timestamp": datetime.now().isoformat(),
        "sender": "user"
    }


@pytest.fixture
def mocked_message_entity(valid_message_data):
    return Message.create_from_dict({
        'id': UUIDField(valid_message_data['message_id']),
        'session_id': UUIDField(valid_message_data['session_id']),
        'content': ContentField(valid_message_data['content']),
        'timestamp': DatetimeField(datetime.now().isoformat()),
        'sender': SenderField(valid_message_data['sender']),
        'word_count': 5,
        'character_count': 26,
        'processed_at': DatetimeField(datetime.now().isoformat())
    })


@pytest.fixture
def mock_user_service():
    return MagicMock()


@pytest.fixture
def mock_user_entity():
    return User.create_from_dict({
        'username': UsernameField('testuser'),
        'email': EmailField('test@example.com')
    })
