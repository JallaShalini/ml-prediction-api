from io import BytesIO
from pathlib import Path

import requests
from PIL import Image

img = Image.new('RGB', (64, 64), color='blue')
buf = BytesIO()
img.save(buf, format='PNG')
data = buf.getvalue()

response = requests.post('http://127.0.0.1:8000/predict', files={'file': ('sample.png', data, 'image/png')}, timeout=120)
Path('predictions/live_prediction.json').write_text(response.text, encoding='utf-8')
print(response.status_code)
print(response.text)
