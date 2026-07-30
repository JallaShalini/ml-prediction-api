# Docker

The project includes a Dockerfile and Docker Compose configuration for running the API in a container.

## Build the image

```bash
docker build -t ml-prediction-api:local .
```

## Run with Docker Compose

```bash
docker compose up --build
```

The service listens on port `8000` and exposes the health endpoint at:

```text
http://127.0.0.1:8000/health
```

## Container details

- the model artifacts are mounted from the `models/` directory
- the container uses a Python runtime and starts the FastAPI app with `uvicorn`
- the compose file includes a health check for `/health`

## Useful commands

```bash
docker compose ps
docker compose logs -f api
docker compose down
```
