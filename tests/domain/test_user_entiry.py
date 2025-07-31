import uuid
from datetime import datetime
from app.domain.entities.user import User
from app.domain.value_objects import (
    UUIDField,
    EmailField,
    UsernameField,
    PasswordHashField
)


class TestUserEntity:
    def test_user_creation_with_valid_data(
            self,
            valid_email_str,
            valid_username_str,
            valid_password_hash_str
            ):
        """create a User entity with all valid data succesfully."""
        email = EmailField(valid_email_str)
        username = UsernameField(valid_username_str)
        password_hash = PasswordHashField(valid_password_hash_str)

        user = User(
            email=email,
            username=username,
            password_hash=password_hash,
        )

        assert isinstance(user.id, uuid.UUID)
        assert user.email == email
        assert user.username == username
        assert user.password_hash == password_hash
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_user_create_from_dict_method(
            self,
            valid_uuid_str,
            valid_email_str,
            valid_username_str,
            valid_password_hash_str
            ):
        """Create a User instance from a dictionary correctly."""
        now = datetime.utcnow()
        user_data = {
            "id": UUIDField(valid_uuid_str),
            "email": EmailField(valid_email_str),
            "username": UsernameField(valid_username_str),
            "password_hash": PasswordHashField(valid_password_hash_str),
            "created_at": now,
            "updated_at": now
        }
        user = User.create_from_dict(user_data)

        assert str(user.id.value) == valid_uuid_str
        assert user.email.value == valid_email_str
        assert user.username.value == valid_username_str
        assert user.password_hash.value == valid_password_hash_str
        assert user.created_at == now
        assert user.updated_at == now

    def test_user_to_dict_method(
            self,
            valid_email_str,
            valid_username_str,
            valid_password_hash_str
            ):
        """convert the User entity to a dictionary correctly."""
        user = User(
            email=EmailField(valid_email_str),
            username=UsernameField(valid_username_str),
            password_hash=PasswordHashField(valid_password_hash_str)
        )
        user_dict = user.to_dict()

        assert isinstance(user_dict, dict)
        assert user_dict["email"] == valid_email_str
        assert user_dict["username"] == valid_username_str
