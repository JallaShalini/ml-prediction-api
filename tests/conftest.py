import pytest

from src.model import load_model


@pytest.fixture(autouse=True)
def clear_model_cache() -> None:
    load_model.cache_clear()
    yield
    load_model.cache_clear()
