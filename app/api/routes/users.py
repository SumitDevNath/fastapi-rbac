from fastapi import APIRouter, Depends, status
from app.db.models import User
from app.dependencies.auth import get_current_user
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Current Authenticated User Profile"
)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    """
    Returns the profile of the currently logged-in user.
    Requires a valid Bearer JWT token.
    """
    return current_user