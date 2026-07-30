from io import BytesIO
from unittest.mock import patch

import pytest
from PIL import Image

from src.services.inference_service import InferenceService


@pytest.fixture
def service() -> InferenceService:
    return InferenceService()


def test_empty_payload_is_rejected(service: InferenceService) -> None:
    with pytest.raises(ValueError, match="empty"):
        service.validate_image(b"", "test.png")


def test_invalid_content_type_is_rejected(service: InferenceService) -> None:
    payload = b"not-an-image"
    with pytest.raises(ValueError, match="Only image files"):
        service.validate_image(payload, "test.txt")


def test_corrupt_image_is_rejected(service: InferenceService) -> None:
    with pytest.raises(ValueError, match="Invalid image file"):
        service.validate_image(b"not an image", "test.png")


def test_prediction_service_uses_prediction_pipeline(service: InferenceService) -> None:
    image = Image.new("RGB", (64, 64), color="blue")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    payload = buffer.getvalue()

    with patch("src.services.inference_service.predict_image", return_value={"class_label": "cat", "probabilities": [0.9, 0.1]}) as mock_predict:
        result = service.predict_from_bytes(payload, "test.png")

    assert result["class_label"] == "cat"
    assert result["probabilities"] == [0.9, 0.1]
    mock_predict.assert_called_once()
