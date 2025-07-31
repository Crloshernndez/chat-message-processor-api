import pytest
from app.domain.value_objects import UsernameField
from app.domain.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


class TestUsernameField:
    def test_valid_username_creation(self, valid_username_str):
        """Create an UsernameField with a valid username successfully."""
        username_field = UsernameField(valid_username_str)
        assert username_field.value == valid_username_str
        assert str(username_field) == valid_username_str

    def test_empty_username_error(self):
        """Should throw RequiredFieldException for empty value."""
        with pytest.raises(RequiredFieldException) as excinfo:
            UsernameField('')

        assert "El campo de username es requerido." in str(
            excinfo.value.message
            )

    def test_to_short_username_error(self):
        """Should throw DomainValidationException for shorts usernames."""
        with pytest.raises(DomainValidationException) as excinfo:
            UsernameField("a")

        error_detail = (
            "El nombre de usuario 'a' debe tenerentre 3 y 30 caracteres."
        )
        assert error_detail in str(excinfo.value.detail)

    def test_to_large_username_error(self):
        """Should throw DomainValidationException for larges usernames."""
        long_username = ("a" * 31)
        with pytest.raises(DomainValidationException) as excinfo:
            UsernameField(long_username)

        error_detail = (
            f"El nombre de usuario '{long_username}' \
debe tenerentre 3 y 30 caracteres."
        )
        assert error_detail in str(excinfo.value.detail)

    def test_invalid_email_format(self):
        """Should throw DomainValidationException for invalid username."""
        invalid_username = "example()"
        with pytest.raises(DomainValidationException) as excinfo:
            UsernameField(invalid_username)

        error_detail = (
            f"El nombre de usuario '{invalid_username}' \
solo puede contener letras, números, guiones bajos y puntos."
        )
        assert error_detail in excinfo.value.detail
