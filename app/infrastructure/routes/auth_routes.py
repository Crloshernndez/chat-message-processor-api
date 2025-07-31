from typing import Dict, Any
from fastapi import APIRouter, Depends, status
from app.services.user_service import UserService, get_user_service
from app.core.security import create_access_token
from app.infrastructure.decorators import handle_api_exceptions

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid input or domain validation error."
            },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error."
            }
    }
)
@handle_api_exceptions
async def login_for_access_token(
    form_data: Dict[str, Any],
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.authenticate_user(form_data)

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
        }
