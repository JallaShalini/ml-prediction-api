# API examples

The service exposes two primary endpoints:

- `GET /health` for liveness checks
- `POST /predict` for image classification

## Swagger UI

Open the interactive docs at:

```text
http://127.0.0.1:8000/docs
```

## Health check example

```bash
curl http://127.0.0.1:8000/health
```

Example response:

```json
{
  "status": "ok",
  "message": "API is healthy"
}
```

## Prediction example

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -F "file=@sample_images/cat.png;type=image/png"
```

Example response:

```json
{
  "class_label": "automobile",
  "probabilities": [0.03, 0.41, 0.12, 0.28]
}
```

## Python example

```python
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image

img = Image.new("RGB", (64, 64), color="blue")
buffer = BytesIO()
img.save(buffer, format="PNG")
data = buffer.getvalue()

response = requests.post(
    "http://127.0.0.1:8000/predict",
    files={"file": ("sample.png", data, "image/png")},
    timeout=120,
)
print(response.json())
```
