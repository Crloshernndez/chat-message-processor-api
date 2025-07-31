import pytest
from app.domain.value_objects import EmailField
from app.domain.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


class TestEmailField:
    def test_valid_email_creation(self, valid_email_str):
        """Create an EmailField with a valid email address successfully."""
        email_field = EmailField(valid_email_str)
        assert email_field.value == valid_email_str
        assert str(email_field) == valid_email_str

    def test_empty_email_error(self):
        """Should throw RequiredFieldException for empty value."""
        with pytest.raises(RequiredFieldException) as excinfo:
            EmailField('')

        assert "El campo de email es requerido." in str(excinfo.value.message)

    def test_invalid_email_string(self):
        """Should throw DomainValidationException for invalid email."""
        with pytest.raises(DomainValidationException) as excinfo:
            EmailField("invalidemail.com")

        assert "Formato de email invalido." in str(excinfo.value.message)
