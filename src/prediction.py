import numpy as np

from src.model import load_labels, load_model
from src.preprocessing import preprocess_image


def predict_image(image_bytes: bytes) -> dict[str, object]:
    preprocessed = preprocess_image(image_bytes)
    model = load_model()
    probabilities = model.predict(preprocessed, verbose=0)[0]
    predicted_index = int(np.argmax(probabilities))
    labels = load_labels()
    label = labels[predicted_index] if 0 <= predicted_index < len(labels) else "unknown"

    return {
        "class_label": label,
        "probabilities": [float(value) for value in probabilities.tolist()],
    }
