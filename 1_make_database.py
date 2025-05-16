# Pull the latest prices from amazon.jp and store them in a text file to be
# used as a database for the RAG model.

import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from py_markdown_table.markdown_table import markdown_table
import re
import wikipedia

def get_first_sentence(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    return sentences[0]

def translate_to_english(translator, text):
    # Placeholder function for translation
    # In a real scenario, you would use a translation API or library
    return translator.translate(text)

custom_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}
# Link for Pocari sweat on kakaku.com
target_url = "https://search.kakaku.com/%E3%83%9D%E3%82%AB%E3%83%AA%E3%82%B9%E3%82%A8%E3%83%83%E3%83%88/"
response = requests.get(target_url, headers=custom_headers)
soup = BeautifulSoup(response.text, "html.parser")
translator = GoogleTranslator(source='ja', target='en')
wiki = wikipedia.page("Pocari Sweat")

product_summary = get_first_sentence(wiki.content)
product_price = soup.find(class_="p-item_priceNum").text.strip()
product_name = soup.find(class_="p-item_name s-biggerlinkHover_underline").text.strip()
seller = soup.find(class_="p-resultItem_quote").text.strip()
# Print the product name and pric
data = [
    {
        "Product Name (JP)": product_name,
        "Product Name (EN)": translate_to_english(translator, product_name),
        "Price": product_price,
        "Seller": seller,
        "Summary": product_summary,
    }
]

markdown = markdown_table(data).get_markdown()

with open("kakaku_prices.md", "w") as f:
    f.write(markdown)