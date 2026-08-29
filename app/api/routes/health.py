from fastapi import APIRouter, status

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Returns the operational status of the API server."
)
def check_health():
    return {
        "status": "healthy",
        "service": "fastapi-auth-system",
        "version": "1.0.0"
    }