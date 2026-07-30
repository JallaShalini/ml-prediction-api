from io import BytesIO

from PIL import Image

from src.config import settings


def load_image_from_bytes(image_bytes: bytes) -> Image.Image:
    with Image.open(BytesIO(image_bytes)) as image:
        image.load()
        return image.convert("RGB")


def resize_image(image: Image.Image) -> Image.Image:
    target_width, target_height = settings.image_size
    return image.resize((target_width, target_height))
