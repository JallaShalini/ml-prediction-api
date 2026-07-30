import json
import os
from pathlib import Path

import tensorflow as tf

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

SEED = 42
tf.keras.utils.set_random_seed(SEED)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODELS_DIR / "my_classifier_model.h5"
LABELS_PATH = MODELS_DIR / "labels.json"

CLASS_LABELS = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]

print("Loading CIFAR-10 dataset...")
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
y_train = y_train.flatten()
y_test = y_test.flatten()

x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

print("Building CNN model...")
model = tf.keras.Sequential(
    [
        tf.keras.layers.Input(shape=(32, 32, 3)),
        tf.keras.layers.Conv2D(32, 3, padding="same", activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, padding="same", activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(128, 3, padding="same", activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(len(CLASS_LABELS), activation="softmax"),
    ],
    name="cifar10_classifier",
)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_accuracy",
    patience=2,
    restore_best_weights=True,
)

print("Training model...")
history = model.fit(
    x_train,
    y_train,
    validation_split=0.1,
    epochs=2,
    batch_size=128,
    callbacks=[early_stopping],
    verbose=1,
)

print("Evaluating model...")
test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
print(f"Test loss: {test_loss:.4f}")
print(f"Test accuracy: {test_accuracy:.4f}")

print("Saving model artifacts...")
model.save(MODEL_PATH, save_format="h5")
LABELS_PATH.write_text(json.dumps(CLASS_LABELS, indent=2), encoding="utf-8")

loaded_model = tf.keras.models.load_model(MODEL_PATH)
loaded_labels = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
assert MODEL_PATH.exists() and MODEL_PATH.stat().st_size > 0
assert LABELS_PATH.exists() and loaded_labels == CLASS_LABELS
assert loaded_model.output_shape[-1] == len(loaded_labels)

print(f"Saved model: {MODEL_PATH}")
print(f"Saved labels: {LABELS_PATH}")
print(f"Model artifact size: {MODEL_PATH.stat().st_size:,} bytes")
print("Artifacts verified successfully.")
