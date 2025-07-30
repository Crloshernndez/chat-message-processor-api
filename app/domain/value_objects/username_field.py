from dataclasses import dataclass
import re
from app.domain.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


@dataclass(frozen=True)
class UsernameField:
    value: str

    def __post_init__(self):
        if not self.value:
            raise RequiredFieldException(
                field_name="username",
                message="El nombre de usuario no puede estar vacío."
            )

        self._validate()

    def _validate(self) -> None:
        if not (3 <= len(self.value) <= 30):
            raise DomainValidationException(
                f"El nombre de usuario '{self.value}' debe tener\
                    entre 3 y 30 caracteres.",
                field="username"
            )

        if not re.match(r"^[a-zA-Z0-9_.]+$", self.value):
            raise DomainValidationException(
                f"El nombre de usuario '{self.value}' solo puede\
                    contener letras, números, guiones bajos y puntos.",
                field="username"
            )

    def __str__(self) -> str:
        """
        Devuelve la representación en cadena del nombre de usuario.
        """
        return self.value
