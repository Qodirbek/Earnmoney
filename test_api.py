import requests

API_KEY = "daf559389emsh3033de07bea550dp1a10bajsn2adbbb1023d2"
API_HOST = "aliexpress-datahub.p.rapidapi.com"

# API to‘g‘ri ishlaydigan endpoint va parametrlari
API_URL = "https://aliexpress-datahub.p.rapidapi.com/item_search"

params = {
    "q": "laptop",  # ❗ E'tibor bering: "q" parametri talab qilinmoqda
    "page": 1
}

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

response = requests.get(API_URL, headers=headers, params=params)

# API javobini ekranga chiqarish
print(response.json())
