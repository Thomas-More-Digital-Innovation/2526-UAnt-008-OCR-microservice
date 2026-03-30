# OCR_SERVICE
<p align="center">
  <img src="https://github.com/user-attachments/assets/677d879c-7a61-4eff-9e00-28c08e4bda32" width="300"/>
</p>

# General information
An OCR service to get text of images. Hosted in a docker. The Python code is written in PEP8 style.

## Usage of OCR service
1. Clone this repository to your local machine.
2. Make sure Docker and docker-compose are installed.
3. Start the service:
   ```sh
   docker compose up -d
   ```
   The service runs on port 8000 by default.
4. Want to use a different port? Change PORT in the `.env` file and restart:
   ```env
   PORT=12345
   ```
5. Send a POST request to `/ocr?method=easyocr` or `/ocr?method=tesseract` with an image.
6. You will receive the recognized text as JSON.

Made by Maurits Groen
