from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from src.model import load_model


@patch("src.model.tf.keras.models.load_model")
def test_load_model_uses_cached_model(mock_load_model) -> None:
    mock_model = Mock()
    mock_load_model.return_value = mock_model
    load_model.cache_clear()

    fake_settings = SimpleNamespace(
        absolute_model_path=Path("fake_model.h5"),
        absolute_labels_path=Path("fake_labels.json"),
    )

    with patch("src.model.settings", new=fake_settings), patch("src.model.Path.exists", return_value=True):
        first_result = load_model()
        second_result = load_model()

    assert first_result is mock_model
    assert second_result is mock_model
    assert mock_load_model.call_count == 1
