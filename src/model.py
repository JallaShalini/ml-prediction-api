import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import tensorflow as tf

from src.config import settings


@lru_cache(maxsize=1)
def load_model() -> tf.keras.Model:
    model_path = settings.absolute_model_path
    labels_path = settings.absolute_labels_path

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not labels_path.exists():
        raise FileNotFoundError(f"Labels file not found: {labels_path}")

    model = tf.keras.models.load_model(model_path)
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


def load_labels() -> list[str]:
    labels_path = settings.absolute_labels_path
    with labels_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
