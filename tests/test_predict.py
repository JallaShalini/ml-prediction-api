from io import BytesIO

from PIL import Image
from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_predict_endpoint_with_valid_image() -> None:
    image = Image.new("RGB", (64, 64), color="blue")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    response = client.post(
        "/predict",
        files={"file": ("test.png", buffer.read(), "image/png")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "class_label" in payload
    assert "probabilities" in payload
    assert isinstance(payload["probabilities"], list)
