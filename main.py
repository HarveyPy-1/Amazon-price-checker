import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

# ----------------------------------------- CONSTANTS ----------------------------------------- #
URL = "https://www.amazon.co.uk/Soundcore-Bluetooth-Technology-Waterproof-Customizable/dp/B08FCDFHLB/ref=sr_1_10?crid=5HLV97STUD21&keywords=anker+speaker&qid=1683318742&sprefix=anker+speaker%2Caps%2C114&sr=8-10"
my_email = "harveyezihe@gmail.com"
password = "securepassword"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 "
                  "Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"'
}

# ----------------------------------- ACCESS WEBPAGE AND MAKE SOUP ----------------------------------- #
response = requests.get(url=URL, headers=headers)

soup = BeautifulSoup(response.text, "lxml")

# ------------------------------- SCRAPE WEBPAGE AND GET CURRENT PRICE ------------------------------- #
price_location = soup.select_one(selector=".a-offscreen")
current_price = float(price_location.getText().split("£")[1])

# ---------------------------- COMPARE PRICES AND SEND MAIL NOTIFICATION ----------------------------- #
email_string = f"The price of the Anker Speaker you wanted has just dropped to £ {current_price}, " \
               f"which is below your preferred price. Click the link below to buy now:"

encoded_email_string = email_string.encode("utf-8")


def compare_prices():
    if current_price <= 28:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="my_email",
                msg=f"Subject:AMAZON PRICE DROP ALERT!\n\n{encoded_email_string} \n\n{URL}"
            )
            print("Email Sent!")
    else:
        print(f"£{current_price}")


compare_prices()
