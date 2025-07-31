from dataclasses import dataclass
import re
from app.domain.exceptions import RequiredFieldException


@dataclass(frozen=True)
class ContentField:
    value: str

    INAPPROPRIATE_WORDS = ["malo", "ofensivo", "prohibido", "spam"]

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise RequiredFieldException(
                message="El campo de content es requerido.",
                detail="El campo de content no puede ser nulo.",
                )

        self._validate_and_filter()

    def _validate_and_filter(self) -> None:
        cleaned_content = self.value

        for word in self.INAPPROPRIATE_WORDS:
            cleaned_content = re.sub(
                re.escape(word),
                '***',
                cleaned_content,
                flags=re.IGNORECASE
                )

        object.__setattr__(self, 'value', cleaned_content)
