import pytest
from app.domain.value_objects import PasswordRawField
from app.domain.exceptions import (
    DomainValidationException
)


class TestPasswordRawField:
    def test_valid_password_raw_creation(self, valid_password_raw_str):
        """Debe crear un PasswordField con un hash de contraseña válido."""
        password_field = PasswordRawField(valid_password_raw_str)
        assert password_field.value == valid_password_raw_str
        assert str(password_field.value) == valid_password_raw_str

    def test_to_short_password_error(self):
        """Should throw DomainValidationException for shorts passworrd."""
        with pytest.raises(DomainValidationException) as excinfo:
            PasswordRawField("aB12")

        error_detail = (
            "La contraseña debe tener al menos 6 caracteres."
        )
        assert error_detail in str(excinfo.value.detail)

    def test_to_large_password_error(self):
        """Should throw DomainValidationException for large password."""
        long_password = ("aB1" * 50)

        with pytest.raises(DomainValidationException) as excinfo:
            PasswordRawField(long_password)

        error_detail = (
            "La contraseña no puede tener más de 128 caracteres."
        )
        assert error_detail in str(excinfo.value.detail)

    def test_to_without_capital_letter_password_error(self):
        """Should throw DomainValidationException for no capital\
            letter password."""
        with pytest.raises(DomainValidationException) as excinfo:
            PasswordRawField("a123456z")

        error_detail = (
            "La contraseña debe contener al menos una mayúscula."
        )
        assert error_detail in str(excinfo.value.detail)

    def test_to_without_lowercase_letter_password_error(self):
        """Should throw DomainValidationException for no lowercase\
            letter password."""
        with pytest.raises(DomainValidationException) as excinfo:
            PasswordRawField("A123456Z")

        error_detail = (
            "La contraseña debe contener al menos una minúscula."
        )
        assert error_detail in str(excinfo.value.detail)

    def test_to_without_number_characters_password_error(self):
        """Should throw DomainValidationException for no number\
            password password."""
        with pytest.raises(DomainValidationException) as excinfo:
            PasswordRawField("AbcdefgZ")

        error_detail = (
            "La contraseña debe contener al menos un número."
        )
        assert error_detail in str(excinfo.value.detail)
