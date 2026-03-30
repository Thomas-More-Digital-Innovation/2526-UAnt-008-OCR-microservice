import requests

response = requests.post("http://localhost:8000/ocr/path", params={
    "image": "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/macdonald-food-flyer-design-template-24c9c95357b4c3677b5f7702199a2f56_screen.jpg?ts=1676201110",
    "method": "easyocr"
})
print(response.json()) 