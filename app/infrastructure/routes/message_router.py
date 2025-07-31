from typing import Dict, Any, Optional
from fastapi import (
    APIRouter,
    Depends,
    status,
    Query
)
from app.services.message_service import (
    MessageService,
    get_message_service
)
from app.infrastructure.decorators import handle_api_exceptions

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post(
    "/",
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
async def register_message_endpoint(
    message_data: Dict[str, Any],
    message_service: MessageService = Depends(get_message_service)
):
    new_message_entity = message_service.register_message(message_data)

    return new_message_entity.to_dict()


@router.get(
    "/detail/{message_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid message ID format."
            },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid input or domain validation error."
            },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error."
            }
    }
)
@handle_api_exceptions
async def get_message_by_id_endpoint(
    message_id: str,
    message_service: MessageService = Depends(get_message_service)
):
    message_entity = message_service.get_message_by_id(message_id)

    return message_entity.to_dict()


@router.get(
    "/{session_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid message ID format."
            },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid input or domain validation error."
            },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error."
            }
    }
)
@handle_api_exceptions
async def get_message_by_session_endpoint(
    session_id: str,
    limit: Optional[int] = Query(default=50, ge=1, le=100, description="Number of messages to return"),
    offset: Optional[int] = Query(default=0, ge=0, description="Number of messages to skip"),
    sender: Optional[str] = Query(default=None, description="Filter by sender"),
    message_service: MessageService = Depends(get_message_service)
):
    message_entities, total_count = message_service.get_message_by_session_id(
        session_id=session_id,
        limit=limit,
        offset=offset,
        sender=sender
        )

    return {
        "messages": (
            [message.to_dict() for message in message_entities]
        ),
        "pagination": {
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "has_next": offset + limit < total_count,
            "has_previous": offset > 0
        }
    }
