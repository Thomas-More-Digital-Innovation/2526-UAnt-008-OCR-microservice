import importlib
from io import BytesIO

from PIL import Image, ImageDraw
import main

# Create a TestClient for the FastAPI app
TestClient = importlib.import_module('fastapi.testclient').TestClient
client = TestClient(main.app)


# Test the root endpoint
def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'text': 'The OCR service is running!'}


# This function creates a simple PNG image with text
def _sample_png_bytes(text='TEST'):
    img = Image.new('RGB', (240, 90), color='white')
    ImageDraw.Draw(img).text((20, 30), text, fill='black')
    buf = BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


# Test the easyocr endpoint with an image
def test_easyocr():
    response = client.post(
        '/ocr?method=easyocr',
        files={'image': ('ocr-test.png', _sample_png_bytes(), 'image/png')},
    )
    assert response.status_code == 200
    body = response.json()
    assert 'error' not in body
    assert isinstance(body.get('text'), str)


# Test the tesseract endpoint with an image
def test_tesseract():
    response = client.post(
        '/ocr?method=tesseract',
        files={'image': ('ocr-test.png', _sample_png_bytes(), 'image/png')},
    )
    assert response.status_code == 200
    body = response.json()
    assert 'error' not in body
    assert isinstance(body.get('text'), str)
