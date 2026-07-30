from pathlib import Path
import requests
import webbrowser

API_URL = "http://127.0.0.1:8000"
DOCS_URL = f"{API_URL}/docs"

p = Path(__file__).resolve().parents[1] / "sample_images" / "cat.png"
if not p.exists():
    print("sample_images/cat.png not found at", p)
    raise SystemExit(1)

print("Posting", p)
try:
    r = requests.post(
        f"{API_URL}/predict",
        files={"file": (p.name, p.read_bytes(), "image/png")},
        timeout=30,
    )
except Exception as exc:
    print("Request failed:", exc)
    raise

print("Status:", r.status_code)
print(r.text)

print("Opening Swagger UI at", DOCS_URL)
webbrowser.open(DOCS_URL)
