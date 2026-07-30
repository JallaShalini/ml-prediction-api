from io import BytesIO

from PIL import Image, UnidentifiedImageError


def validate_empty_file(image_bytes: bytes) -> None:
    if not image_bytes:
        raise ValueError("Image payload is empty")


def validate_file_size(image_bytes: bytes, max_bytes: int) -> None:
    if len(image_bytes) > max_bytes:
        raise ValueError("Image payload exceeds maximum allowed size")


def validate_mime_type(content_type: str | None) -> None:
    if not content_type or not content_type.startswith("image/"):
        raise ValueError("Only image files are allowed")


def validate_image_bytes(image_bytes: bytes) -> tuple[int, int]:
    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image.verify()
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("Invalid image file") from exc

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image.load()
            return image.size
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("Invalid image file") from exc


def validate_dimensions(width: int, height: int, min_width: int = 1, min_height: int = 1) -> None:
    if width < min_width or height < min_height:
        raise ValueError("Image dimensions are invalid")
