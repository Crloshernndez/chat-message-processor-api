import pytest
from app.domain.value_objects import ContentField
from app.domain.exceptions import (
    RequiredFieldException
)


class TestContentField:
    def test_valid_content_creation(self, valid_content_str):
        """You must create a ContentField with a valid, clean string."""
        content_field = ContentField(valid_content_str)
        assert content_field.value == valid_content_str
        assert str(content_field.value) == valid_content_str

    def test_whitespace_string_raises_required_field_exception(self):
        """Must throw RequiredFieldException for a content string with\
            only spaces."""
        with pytest.raises(RequiredFieldException) as excinfo:
            ContentField("   ")
        assert "El campo de content es requerido." in str(excinfo.value)

    def test_inappropriate_word_is_filtered(
              self,
              content_with_inappropriate_words
              ):
        """Debe reemplazar una palabra inapropiada con '***'."""
        content_field = ContentField(content_with_inappropriate_words)
        expected_value = "Este es un mensaje *** y ***."
        assert content_field.value == expected_value
