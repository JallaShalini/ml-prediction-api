import io
from typing import Any

import numpy as np
from PIL import Image, UnidentifiedImageError

from src.config import settings


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except UnidentifiedImageError as exc:
        raise ValueError("Unable to read image data") from exc

    target_height, target_width = settings.image_size
    image = image.resize((target_width, target_height))
    image_array = np.asarray(image, dtype=np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array
