# #################   IMPORTS AND INITIALIZATION    ########################
from abc import ABC, abstractmethod
from PIL import Image
from fastapi import FastAPI, UploadFile, File
import io
import easyocr
import pytesseract

app = FastAPI()


# ######################    OCR CLASSES    ################################
class BaseOCR(ABC):
    """Abstact base class for OCR implementations"""
    @abstractmethod
    def read_text(self, image) -> str:
        pass


class EasyOCR(BaseOCR):
    """Implementation of OCR using EasyOCR"""
    def __init__(self):
        self.reader = easyocr.Reader(['en', 'fr', 'de', 'it', 'nl'], gpu=False)

    def read_text(self, image) -> str:
        result = self.reader.readtext(image)
        text_only = ' '.join(text for bbox, text, conf in result)
        return text_only


class TesseractOCR(BaseOCR):
    """Implementation of OCR using Tesseract"""
    def __init__(self):
        self.pytesseract = pytesseract

    def read_text(self, image) -> str:
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


@app.post('/ocr')
async def ocr(image: UploadFile = File(...), method: str = 'easyocr'):
    if method not in ocr_readers:
        return {'error': f'Unsupported OCR method: {method}'}
    try:
        contents = await image.read()

        if method == 'easyocr':
            text = ocr_readers[method].read_text(contents)
        else:
            pil_image = Image.open(io.BytesIO(contents))
            text = ocr_readers[method].read_text(pil_image)

        return {'text': text}
    except Exception as e:
        return {'error': str(e)}
