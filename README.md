# ml-prediction-api

This repository hosts a FastAPI image classification service that serves a trained CIFAR-10-style model for predicting image classes from uploaded files.

## What the service does

- exposes a health endpoint at `/health`
- accepts image uploads at `/predict`
- validates image payloads before inference
- returns the predicted class label and a probability vector
- can be run locally or in Docker

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the API:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```
4. Open the interactive docs at `http://127.0.0.1:8000/docs`.

## Example requests

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Prediction request:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -F "file=@sample_images/cat.png;type=image/png"
```

## Repository layout

- `src/` contains the FastAPI app, prediction pipeline, validation helpers, and service layer.
- `models/` stores the trained model and labels.
- `predictions/` contains generated example payloads.
- `docs/` contains architecture, API examples, Docker, CI/CD notes, and screenshots.

## Testing

Run the test suite:

```bash
pytest -q
```

## Documentation

- [docs/architecture.md](docs/architecture.md)
- [docs/api_examples.md](docs/api_examples.md)
- [docs/docker.md](docs/docker.md)
- [docs/cicd.md](docs/cicd.md)
