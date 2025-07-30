from dataclasses import dataclass
from app.domain.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


@dataclass(frozen=True)
class PasswordField:
    value: str

    def __post_init__(self):
        if not self.value:
            raise RequiredFieldException(
                field_name="email",
                message="El campo 'email' no puede estar vacío."
                )

        self._validate()

    def _validate(self) -> None:
        if len(self.value) < 6:
            raise DomainValidationException(
                "El hash de la contraseña es demasiado corto.",
                field="password_hash"
            )

    def __str__(self) -> str:
        """
        Devuelve la representación en cadena del hash de la contraseña.
        """
        return self.value
