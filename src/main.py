from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.health import router as health_router
from src.api.predict import router as predict_router
from src.config import settings
from src.logging_config import logger
from src.model import load_model

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Image classification API for serving a CIFAR-10 model",
)

# Allow CORS so the Swagger UI (or other origins) can POST files from browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(predict_router)


@app.get(
    "/",
    status_code=200,
    summary="Root endpoint",
    responses={200: {"description": "Service is healthy"}},
)
def root() -> dict[str, str]:
    return {"status": "ok", "message": "API is healthy"}


@app.on_event("startup")
def startup_event() -> None:
    logger.info("Loading model during startup")
    load_model()
    logger.info("Model loaded successfully")


@app.on_event("shutdown")
def shutdown_event() -> None:
    logger.info("Shutting down application")
