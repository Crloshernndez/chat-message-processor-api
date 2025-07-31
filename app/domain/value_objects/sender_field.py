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
                message="El campo de sender es requerido.",
                detail="El campo de sender no puede ser nulo."
                )

        self._validate()

    def _validate(self) -> None:
        if self.value not in self.VALID_TYPES:
            raise DomainValidationException(
                message="Formato de sender invalido.",
                detail=f"El valor '{self.value}' no es un remitente válido.\
Debe ser 'user' o 'system'.",
                code="INVALID_FORMAT"
            )

    def __str__(self) -> str:
        return self.value
