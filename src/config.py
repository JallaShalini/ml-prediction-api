import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = Field(default="ml-prediction-api")
    app_version: str = Field(default="0.1.0")
    log_level: str = Field(default="INFO")
    model_path: str = Field(default="models/my_classifier_model.h5")
    labels_path: str = Field(default="models/labels.json")
    image_size: tuple[int, int] = Field(default=(64, 64))
    max_upload_size_mb: int = Field(default=5)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    environment: Literal["development", "testing", "production"] = Field(default="development")

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parents[1]

    @property
    def absolute_model_path(self) -> Path:
        path = Path(self.model_path)
        if not path.is_absolute():
            path = self.project_root / path
        return path

    @property
    def absolute_labels_path(self) -> Path:
        path = Path(self.labels_path)
        if not path.is_absolute():
            path = self.project_root / path
        return path

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as exc:
        raise RuntimeError(f"Invalid configuration: {exc}") from exc


settings = get_settings()
