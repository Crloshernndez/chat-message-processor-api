from dataclasses import dataclass
import uuid
from app.domain.exceptions import (
    RequiredFieldException,
    InvalidUUIDException
)


@dataclass(frozen=True)
class UUIDField:
    ID_FIELD_NAME = 'id'
    value: uuid.UUID

    def __post_init__(self):
        self._validate()

    @classmethod
    def from_string(cls, value: str) -> 'UUIDField':
        return cls(value)

    def _validate(self) -> None:
        if not self.value:
            raise RequiredFieldException(
                message="El campo de id es requerido.",
                detail="El campo de id no puede ser nulo."
            )

        if isinstance(self.value, str):
            cleaned_value = self.value.strip()
            try:
                uuid_obj = uuid.UUID(cleaned_value)
                object.__setattr__(self, 'value', uuid_obj)
            except (ValueError, TypeError):
                raise InvalidUUIDException()
        elif not isinstance(self.value, uuid.UUID):
            raise InvalidUUIDException()

    def __str__(self) -> str:
        return str(self.value)
