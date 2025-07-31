from fastapi import APIRouter, Depends, status
from app.services.user_service import (
    UserService,
    get_user_service
)
from app.infrastructure.decorators import handle_api_exceptions
from typing import Dict, Any

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
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
async def register_user_endpoint(
    user_data: Dict[str, Any],
    user_service: UserService = Depends(get_user_service)
):
    new_user_entity = user_service.register_user(user_data)

    return {
        "status": "success",
        "data": new_user_entity.to_dict()
        }
