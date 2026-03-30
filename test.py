import requests

response = requests.post("http://localhost:8000/ocr/path", params={
    "image": "https://i.sstatic.net/0Jl54.png",
    "method": "easyocr"
})
print(response.json())
