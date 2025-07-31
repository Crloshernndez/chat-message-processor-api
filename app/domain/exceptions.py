class BaseApplicationException:
    def __init__(
            self,
            message: str,
            detail: str,
            code: str
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


class DomainValidationException(BaseApplicationException, ValueError):
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
        super().__init__(
            self.message,
            self.detail,
            self.code
        )


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
    def __init__(self):
        self.code = "INVALID_FORMAT"
        self.message = "Formato de ID invalido."
        self.detail = "El valor del ID no es un formato de \
uuid válido."


class InfrastructureException(BaseApplicationException, Exception):
    """
    Base exception for all infrastructure-related errors.
    """
    def __init__(
            self,
            message: str,
            detail: Exception = None,
            code: str = "INFRASTRUCTURE_ERROR"
            ):
        self.message = message
        self.detail = detail
        self.code = code
        super().__init__(
            self.message,
            self.detail,
            self.code
        )


class DatabaseConnectionError(InfrastructureException):
    """
    Exception raised when there's an issue connecting to the database.
    """
    def __init__(
            self,
            message: str = "Error de conexión a la base de datos.",
            detail: Exception = None
            ):
        super().__init__(message, detail)


class DatabaseOperationError(InfrastructureException):
    """
    Exception raised when a database operation
    (e.g., insert, update, delete, query) fails.
    """
    def __init__(
            self,
            message: str = "Error en operación de base de datos.",
            detail: Exception = None):
        super().__init__(message, detail)
