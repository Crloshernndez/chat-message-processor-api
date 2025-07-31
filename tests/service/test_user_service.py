import uuid
import pytest
from app.domain.entities.user import User
from app.domain.value_objects import (
    UUIDField,
    EmailField,
    UsernameField,
    PasswordHashField
)
from app.domain.exceptions import DomainValidationException


class TestUserService:
    def test_register_user_successfully(
            self,
            user_service,
            user_repository_mock,
            valid_user_data,
            valid_password_hash_str
            ):
        """
        must register a user correctly when the data is valid
        and the user does not exist.
        """

        user_repository_mock.get_user_by_email.return_value = None
        user_repository_mock.get_user_by_username.return_value = None

        user_repository_mock.create_user.return_value = User(
            id=UUIDField(uuid.uuid4()),
            email=EmailField(valid_user_data.get("email")),
            username=UsernameField(valid_user_data.get("username")),
            password_hash=PasswordHashField(valid_password_hash_str)
        )

        registered_user = user_service.register_user(valid_user_data)

        user_repository_mock.get_user_by_email.assert_called_once_with(
            EmailField(valid_user_data["email"])
        )
        user_repository_mock.get_user_by_username.assert_called_once_with(
            UsernameField(valid_user_data["username"])
        )

        create_call_args = user_repository_mock.create_user.call_args[0][0]
        assert isinstance(create_call_args, User)
        assert create_call_args.email.value == valid_user_data["email"]

        assert isinstance(registered_user, User)

    def test_register_user_raises_exception_if_email_exists(
            self,
            user_service,
            user_repository_mock,
            valid_user_data,
            mocked_user_entity
            ):
        """
        throw DomainValidationException if a user with the same email
        already exists.
        """
        user_repository_mock.get_user_by_email.return_value = (
            mocked_user_entity
        )
        with pytest.raises(DomainValidationException) as excinfo:
            user_service.register_user(valid_user_data)

        assert "Usuario ya se encuentra registrado" in str(
            excinfo.value.message
            )
        assert excinfo.value.code == "USER_ALREADY_REGISTERED"
        user_repository_mock.get_user_by_email.assert_called_once()
        user_repository_mock.get_user_by_username.assert_not_called()
        user_repository_mock.create_user.assert_not_called()

    def test_register_user_raises_exception_if_username_exists(
        self,
        user_service,
        user_repository_mock,
        valid_user_data,
        mocked_user_entity
    ):
        """
        throw DomainValidationException if a user with the same username
        already exists.
        """
        user_repository_mock.get_user_by_email.return_value = None
        user_repository_mock.get_user_by_username.return_value = (
            mocked_user_entity
        )

        with pytest.raises(DomainValidationException) as excinfo:
            user_service.register_user(valid_user_data)

        assert "Usuario ya se encuentra registrado" in (
            str(excinfo.value.message)
        )
        assert excinfo.value.code == "USER_ALREADY_REGISTERED"
        user_repository_mock.get_user_by_email.assert_called_once()
        user_repository_mock.get_user_by_username.assert_called_once()
        user_repository_mock.create_user.assert_not_called()

    def test_get_user_by_id_successfully(
            self,
            user_service,
            user_repository_mock,
            mocked_user_entity
            ):
        """
        Retrieve a user by their ID when the ID is valid.
        """
        user_id_str = str(mocked_user_entity.id.value)
        user_repository_mock.get_user_by_id.return_value = mocked_user_entity

        retrieved_user = user_service.get_user_by_id(user_id_str)

        user_repository_mock.get_user_by_id.assert_called_once_with(
            UUIDField(user_id_str)
            )
        assert retrieved_user == mocked_user_entity

    def test_authenticate_user_successfully(
            self,
            user_service,
            user_repository_mock,
            valid_user_data,
            mocked_user_entity
            ):
        """
        Authenticate a user with correct credentials.
        """

        user_repository_mock.get_user_by_email.return_value = (
            mocked_user_entity
        )

        authenticated_user = user_service.authenticate_user(valid_user_data)

        user_repository_mock.get_user_by_email.assert_called_once_with(
            EmailField(valid_user_data["email"])
        )
        assert authenticated_user == mocked_user_entity

    def test_authenticate_user_raises_exception_if_user_not_found(
            self,
            user_service,
            user_repository_mock,
            valid_user_data
    ):
        """
        Exception should be thrown if the user is not found by email.
        """
        user_repository_mock.get_user_by_email.return_value = None

        with pytest.raises(DomainValidationException) as excinfo:
            user_service.authenticate_user(valid_user_data)

        assert "Credenciales incorrectas" in str(excinfo.value.message)
        assert excinfo.value.code == "INVALID_CREDENTIALS"
        user_repository_mock.get_user_by_email.assert_called_once()

    def test_authenticate_user_raises_exception_on_incorrect_password(
        self,
        user_service,
        mocked_user_entity,
        user_repository_mock
    ):
        """
        Should throw an exception if the password is incorrect.
        """
        user_repository_mock.get_user_by_email.return_value = (
            mocked_user_entity
        )

        invalid_credentials = {
            "email": mocked_user_entity.email.value,
            "password": "WrongPassword123"
        }

        with pytest.raises(DomainValidationException) as excinfo:
            user_service.authenticate_user(invalid_credentials)

        assert "Credenciales incorrectas" in str(excinfo.value.message)
        assert excinfo.value.code == "INVALID_CREDENTIALS"
        user_repository_mock.get_user_by_email.assert_called_once()
