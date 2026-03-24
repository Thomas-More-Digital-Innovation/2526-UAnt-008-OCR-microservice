# OCR_SERVICE
<p align="center">
  <img src="https://github.com/user-attachments/assets/677d879c-7a61-4eff-9e00-28c08e4bda32" width="300"/>
</p>

# General information
An OCR service to get text of images. Hosted in a docker. The Python code is written in PEP8 style.

## Usage of OCR service
1. Clone deze repository naar je lokale machine.
2. Zorg dat Docker en docker-compose geïnstalleerd zijn.
3. Start de service:
	 ```sh
	 docker compose up -d
	 ```
	 De service draait standaard op poort 8000.
4. Wil je een andere poort? Pas PORT aan in het `.env` bestand en herstart:
	 ```env
	 PORT=12345
	 ```
5. Stuur een POST request naar `/ocr?method=easyocr` of `/ocr?method=tesseract` met een afbeelding.
6. Je krijgt de herkende tekst als JSON terug.

Made by Maurits Groen
