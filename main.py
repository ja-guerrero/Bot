from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

url = "https://shop.flipperzero.one/collections/all/products/flipper-zero"


def test_message():
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body='Your Bot is Listening!',
            from_=+18438944352,
            to=+16463150805
        )
    print(message.sid)


def main_message():
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body=f'FLIPPER ZERO IN STOCK! Please BUY NOW: {url}',
            from_=+18438944352,
            to=+16463150805
        )
    print(message.sid)


def getPage():
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")
    button = soup.find('button', class_='product-form__cart-submit')
    return button


def refresh(button):
    if button.text.strip() == "Sold out":
        print(button.text.strip())
        refresh(getPage())
    else:
        main_message()


if __name__ == "__main__":
    test_message()
    refresh(getPage())
