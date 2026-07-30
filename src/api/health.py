from fastapi import APIRouter, status

from src.schemas import ErrorResponse

router = APIRouter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    responses={200: {"description": "Service is healthy"}, 500: {"model": ErrorResponse}},
)
def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "API is healthy"}
