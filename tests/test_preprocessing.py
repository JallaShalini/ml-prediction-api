from io import BytesIO

import numpy as np
from PIL import Image

from src.preprocessing import preprocess_image
from src.config import settings


def test_preprocess_image_returns_expected_shape() -> None:
    image = Image.new("RGB", (64, 64), color="blue")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    result = preprocess_image(buffer.getvalue())

    assert isinstance(result, np.ndarray)
    assert result.shape == (1, settings.image_size[0], settings.image_size[1], 3)
    assert result.dtype == np.float32
