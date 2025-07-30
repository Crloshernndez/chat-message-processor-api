class DomainValidationException(ValueError):
    """
    Base exception for validation errors within the domain layer.
    """
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

    def to_dict(self):
        """
        Converts the exception to a dictionary for a structured API response.
        """
        return {
            "code": "DOMAIN_VALIDATION_ERROR",
            "message": self.message,
            "details": f"Field affected: {self.field}" if self.field else None
        }


class RequiredFieldException(DomainValidationException):
    """
    Exception raised when a required field is missing or empty in the domain.
    """
    def __init__(self, field_name: str, message: str = None):
        if message is None:
            message = f"The field '{field_name}' is required."
        super().__init__(message, field=field_name)
        self.code = "REQUIRED_FIELD_MISSING"

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "details": f"Missing or empty field: {self.field}"
        }


class InvalidUUIDException(DomainValidationException):
    """
    Exception raised when a value is not a valid UUID format in the domain.
    """
    def __init__(
            self,
            value: str,
            field_name: str = None,
            message: str = None
            ):
        if message is None:
            message = f"The value '{value}' is not a valid UUID."
        super().__init__(message, field=field_name)
        self.value = value
        self.code = "INVALID_UUID_FORMAT"

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "details": f"Invalid UUID value: '{self.value}'" + (
                (f" for field: {self.field}" if self.field else ""))
        }
