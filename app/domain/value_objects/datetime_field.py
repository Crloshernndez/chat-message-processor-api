from dataclasses import dataclass
from datetime import datetime
from app.domain.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


@dataclass(frozen=True)
class DatetimeField:
    value: datetime

    def __post_init__(self):
        if self.value is None:
            raise RequiredFieldException(
                message="El campo de fecha es requerido.",
                detail="El campo de fecha y hora no puede ser nulo."
                )

        self._validate()

    def _validate(self) -> None:
        if not isinstance(self.value, datetime):
            if isinstance(self.value, str):
                try:
                    object.__setattr__(
                        self, 'value',
                        datetime.fromisoformat(
                            self.value.replace('Z', '+00:00')
                            )
                        )
                except ValueError:
                    raise DomainValidationException(
                        message="Formato de fecha invalido.",
                        detail=f"El valor '{self.value}' no es un formato de\
                            fecha y hora ISO 8601 válido.",
                        code="INVALID_FORMAT"
                        )
            else:
                raise DomainValidationException(
                        message="Formato de fecha invalido.",
                        detail=f"El valor '{self.value}' no es un formato de\
                            fecha y hora ISO 8601 válido.",
                        code="INVALID_FORMAT"
                        )

    def __str__(self) -> str:
        return self.value.isoformat()
