# Pull the latest prices from amazon.jp and store them in a text file to be
# used as a database for the RAG model.

import requests
from bs4 import BeautifulSoup

custom_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}
# Link for Pocari sweat on kakaku.com
target_url = "https://search.kakaku.com/%E3%83%9D%E3%82%AB%E3%83%AA%E3%82%B9%E3%82%A8%E3%83%83%E3%83%88/"
response = requests.get(target_url, headers=custom_headers)
soup = BeautifulSoup(response.text, "html.parser")

product_price = soup.find(class_="p-item_priceNum").text.strip()
product_name = soup.find(class_="p-item_name s-biggerlinkHover_underline").text.strip()

# Print the product name and price
print(f"Product Name: {product_name}")
print(f"Product Price: {product_price}")