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
                field_name="DatetimeField.value",
                message="El campo de fecha y hora no puede ser nulo."
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
                        f"El valor '{self.value}' no es un formato de\
                            fecha y hora ISO 8601 válido.",
                        field="DatetimeField.value"
                        )
            else:
                raise DomainValidationException(
                    f"El valor '{self.value}' debe ser un objeto\
                        datetime o una cadena ISO 8601.",
                    field="DatetimeField.value"
                    )

    def __str__(self) -> str:
        return self.value.isoformat()
