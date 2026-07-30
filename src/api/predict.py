from fastapi import APIRouter, File, HTTPException, UploadFile, status

from src.logging_config import logger
from src.schemas import ErrorResponse, PredictionResponse
from src.services.inference_service import InferenceService

router = APIRouter()
inference_service = InferenceService()


@router.post(
    "/predict",
    status_code=status.HTTP_200_OK,
    summary="Predict image class",
    response_model=PredictionResponse,
    responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def predict(file: UploadFile = File(...)) -> PredictionResponse:
    if not file.content_type or not file.content_type.startswith("image/"):
        logger.warning("Rejected upload with unsupported content type: %s", file.content_type)
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    if not file.filename:
        logger.warning("Rejected upload with missing filename")
        raise HTTPException(status_code=400, detail="A filename is required")

    try:
        image_bytes = await file.read()
        result = inference_service.predict_from_bytes(image_bytes, file.filename)
        logger.info("Received prediction request for %s", file.filename)
        return PredictionResponse(**result)
    except ValueError as exc:
        logger.warning("Prediction input validation failed: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive guard
        logger.exception("Prediction failed for %s", file.filename)
        raise HTTPException(status_code=500, detail="Internal server error") from exc
