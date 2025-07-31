class DomainValidationException(ValueError):
    """
    Base exception for validation errors within the domain layer.
    """
    def __init__(
            self,
            message: str,
            detail: str = None,
            code: str = "DOMAIN_VALIDATION_ERROR"
            ):
        self.message = message
        self.detail = detail
        self.code = code
        super().__init__(self.message)

    def to_dict(self):
        """
        Converts the exception to a dictionary for a structured API response.
        """
        return {
            "status": "error",
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.detail
            }
        }


class RequiredFieldException(DomainValidationException):
    """
    Exception raised when a required field is missing or empty in the domain.
    """
    def __init__(self, detail: str, message: str = None):
        super().__init__(message, detail=detail)
        self.code = "REQUIRED_FIELD"


class InvalidUUIDException(DomainValidationException):
    """
    Exception raised when a value is not a valid UUID format in the domain.
    """
    def __init__(
            self,
            value: str,
            detail: str = None,
            message: str = None
            ):
        super().__init__(message, detail=detail)
        self.value = value
        self.code = "INVALID_FORMAT"
        self.message = "Formato de id invalido."
        self.detail = f"El valor '{self.value}' no es un formato de\
                    id válido."
