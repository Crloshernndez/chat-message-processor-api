import pytest
from app.domain.value_objects import SenderField
from app.domain.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


class TestSenderField:
    def test_valid_sender_creation_with_user(self):
        """Create a SenderField with the value 'user'."""
        sender_field = SenderField('user')
        assert sender_field.value == 'user'
        assert str(sender_field) == 'user'

    def test_valid_sender_creation_with_system(self):
        """reate a SenderField with the value 'system'."""
        sender_field = SenderField('system')
        assert sender_field.value == 'system'
        assert str(sender_field) == 'system'

    def test_invalid_sender_raises_domain_validation_exception(self):
        """Throw Domain ValidationException for invalid sender value"""
        with pytest.raises(DomainValidationException) as excinfo:
            SenderField('admin')

        assert "Formato de sender invalido." in str(excinfo.value.message)
        assert "Debe ser 'user' o 'system'." in str(excinfo.value.detail)

    def test_empty_sender_string_raises_required_field_exception(self):
        """Throw RequiredFieldException for an empty sender string."""
        with pytest.raises(RequiredFieldException) as excinfo:
            SenderField("")
        assert "El campo de sender es requerido." in str(excinfo.value.message)

    def test_none_sender_raises_required_field_exception(self):
        """Throw RequiredFieldException for a None sender value."""
        with pytest.raises(RequiredFieldException) as excinfo:
            SenderField(None)
        assert "El campo de sender es requerido." in str(excinfo.value.message)
