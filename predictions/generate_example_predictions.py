import json
import os
from pathlib import Path

import requests
from fastapi.testclient import TestClient

from src.main import app

root = Path(__file__).resolve().parent.parent
api_base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
files_to_generate = [
    ("cat", "cat_prediction.json", "image/png"),
    ("dog", "dog_prediction.json", "image/png"),
    ("airplane", "airplane_prediction.json", "image/png"),
]


def get_prediction_payload(image_path: Path, mime_type: str) -> dict[str, object]:
    image_bytes = image_path.read_bytes()

    try:
        response = requests.post(
            f"{api_base_url}/predict",
            files={"file": (image_path.name, image_bytes, mime_type)},
            timeout=120,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        with TestClient(app) as client:
            response = client.post(
                "/predict",
                files={"file": (image_path.name, image_bytes, mime_type)},
            )
        if response.status_code != 200:
            raise RuntimeError(response.text) from None
        return response.json()


for name, outfile, mime_type in files_to_generate:
    image_path = root / "sample_images" / f"{name}.png"
    output_path = root / "predictions" / outfile
    payload = get_prediction_payload(image_path, mime_type)

    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved {outfile} -> {payload['class_label']}")
