from io import BytesIO
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from src.config import settings
from src.prediction import predict_image
from src.logging_config import logger
from src.utils.validators import validate_empty_file, validate_file_size, validate_mime_type, validate_image_bytes


class InferenceService:
    def __init__(self) -> None:
        self.max_upload_size_bytes = settings.max_upload_size_bytes

    def validate_image(self, image_bytes: bytes, filename: str | None = None) -> None:
        validate_empty_file(image_bytes)
        validate_file_size(image_bytes, self.max_upload_size_bytes)

        if filename:
            suffix = Path(filename).suffix.lower()
            if suffix in {".png", ".jpg", ".jpeg", ".bmp", ".webp"}:
                validate_mime_type(f"image/{suffix.lstrip('.')}" if suffix != ".jpg" else "image/jpeg")
            else:
                raise ValueError("Only image files are allowed")

        validate_image_bytes(image_bytes)

    def predict_from_bytes(self, image_bytes: bytes, filename: str | None = None) -> dict[str, object]:
        self.validate_image(image_bytes, filename)
        logger.info("Processing inference request for %s", filename or "uploaded image")
        prediction = predict_image(image_bytes)
        return {
            "class_label": prediction["class_label"],
            "probabilities": prediction["probabilities"],
        }
