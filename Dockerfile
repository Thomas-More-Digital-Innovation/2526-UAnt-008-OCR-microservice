FROM python:3.12-slim

# install Tesseract OCR + Language packs
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-fra \
    tesseract-ocr-deu \
    tesseract-ocr-ita \
    tesseract-ocr-nld \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# PyTorch CPU
RUN pip install --no-cache-dir torch==2.2.0 --index-url https://download.pytorch.org/whl/cpu

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG PORT=8000
ENV PORT=${PORT}
EXPOSE ${PORT}

# Start de FastAPI server
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]