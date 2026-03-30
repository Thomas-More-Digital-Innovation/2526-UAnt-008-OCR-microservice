# #################   IMPORTS AND INITIALIZATION    ########################
from abc import ABC, abstractmethod
from PIL import Image
import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import io
import easyocr
import pytesseract

app = FastAPI()


# ######################    OCR CLASSES    ################################
class BaseOCR(ABC):
    """Abstact base class for OCR implementations"""
    @abstractmethod
    def read_text(self, image, type) -> str:
        pass


class EasyOCR(BaseOCR):
    """Implementation of OCR using EasyOCR"""
    def __init__(self):
        self.reader = easyocr.Reader(['en', 'fr', 'de', 'it', 'nl'], gpu=False)

    def read_text(self, image, type) -> str:
        # If input is URL path, fetch the image content first
        if type == 'path':
            response = requests.get(image)
            response.raise_for_status()
            image = response.content

        result = self.reader.readtext(image)
        text_only = ' '.join(text for bbox, text, conf in result)
        return text_only


class TesseractOCR(BaseOCR):
    """Implementation of OCR using Tesseract"""
    def __init__(self):
        self.pytesseract = pytesseract

    def read_text(self, image, type) -> str:
        # If input is URL path, fetch the image content first
        if type == 'path':
            response = requests.get(image)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content))
            image.load()

        text_only = self.pytesseract.image_to_string(
            image,
            lang='eng+nld+deu+ita+fra')
        return text_only


# Initialize OCR readers
ocr_readers = {
    'easyocr': EasyOCR(),
    'tesseract': TesseractOCR()
}


# #####################    API ENDPOINTS    ##############################
@app.get('/')
async def root():
    return {'text': 'The OCR service is running!'}


# Endpoint to upload image file for OCR processing
@app.post('/ocr/file')
async def ocr_file(image: UploadFile = File(...), method: str = 'easyocr'):
    if method not in ocr_readers:
        return {'error': f'Unsupported OCR method: {method}'}
    try:
        contents = await image.read()

        if method == 'easyocr':
            text = ocr_readers[method].read_text(contents, 'file')
        else:
            pil_image = Image.open(io.BytesIO(contents))
            text = ocr_readers[method].read_text(pil_image, 'file')

        return {'text': text}
    except Exception as e:
        return {'error': str(e)}


# Endpoint to give image url instead of file upload
@app.post('/ocr/path')
async def ocr_path(image: str, method: str = 'easyocr'):
    if method not in ocr_readers:
        return {'error': f'Unsupported OCR method: {method}'}
    try:
        text = ocr_readers[method].read_text(image, 'path')
        return {'text': text}
    except Exception as e:
        return {'error': str(e)}


# Endpoint with a test image
@app.get('/test_image')
async def test_image():
    image_path = '/app/TEST.Png'
    return FileResponse(image_path, media_type='image/png')
