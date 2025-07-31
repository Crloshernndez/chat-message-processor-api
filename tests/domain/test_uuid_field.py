import uuid
import pytest
from app.domain.value_objects import UUIDField
from app.domain.exceptions import (
    InvalidUUIDException,
    RequiredFieldException
)


class TestUUIDField:
    def test_valid_uuid_creation(self, valid_uuid_str):
        """Create a UUIDField with a valid UUID string successfully."""
        uuid_field = UUIDField(valid_uuid_str)

        assert isinstance(uuid_field.value, uuid.UUID)
        assert str(uuid_field) == valid_uuid_str

    def test_empty_uuid_error(self):
        """Should throw RequiredFieldException for empty value."""
        with pytest.raises(RequiredFieldException) as excinfo:
            UUIDField('')

        assert "El campo de ID es requerido." in str(excinfo.value.message)

    def test_invalid_uuid_string(self):
        """Should throw InvalidUUIDException for an invalid UUID string."""
        with pytest.raises(InvalidUUIDException) as excinfo:
            UUIDField("invalid-uuid-string")

        assert "Formato de ID invalido." in str(excinfo.value.message)
