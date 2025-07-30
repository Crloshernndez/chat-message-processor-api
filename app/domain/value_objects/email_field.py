from dataclasses import dataclass
import re
from app.domain.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


@dataclass(frozen=True)
class EmailField:
    value: str

    def __post_init__(self):
        if not self.value:
            raise RequiredFieldException(
                field_name="email",
                message="El campo 'email' no puede estar vacío."
                )

        self._validate()

    def _validate(self) -> None:
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(email_regex, self.value):
            raise DomainValidationException(
                f"El formato del email '{self.value}' no es válido.",
                field="email"
                )

    def __str__(self):
        return self.value
