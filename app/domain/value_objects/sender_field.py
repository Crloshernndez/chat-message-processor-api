from dataclasses import dataclass
from typing import Literal
from app.domain.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


@dataclass(frozen=True)
class SenderField:
    VALID_TYPES = ('user', 'system')
    value: Literal['user', 'system']

    def __post_init__(self):
        if not self.value:
            raise RequiredFieldException(
                field_name="sender",
                message="El campo 'sender' no puede estar vacío."
                )

        self._validate()

    def _validate(self) -> None:
        if self.value not in self.VALID_TYPES:
            raise DomainValidationException(
                f"El valor '{self.value}' no es un remitente válido.\
                    Debe ser 'user' o 'system'.",
                field="sender"
            )

    def __str__(self) -> str:
        return self.value
