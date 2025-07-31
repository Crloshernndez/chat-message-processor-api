from functools import wraps
from typing import Callable, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from app.domain.exceptions import DatabaseOperationError


def exception_repository_handlers(
    operation_name: Optional[str] = None,
):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs) -> Any:
            try:
                return func(self, *args, **kwargs)

            except SQLAlchemyError as e:
                raise DatabaseOperationError(
                    message=(
                        f"Fallo al crear {operation_name} en base de datos."
                    ),
                    detail=str(e),
                    code="DATABASE_OPERATION_ERROR",
                )

            except Exception as e:
                raise DatabaseOperationError(
                    message=f"Error inesperado al crear {operation_name}",
                    detail=str(e),
                    code="UNEXPECTED_DATABASE_ERROR",
                )

        return wrapper
    return decorator
