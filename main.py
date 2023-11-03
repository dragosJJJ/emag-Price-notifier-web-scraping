import requests,smtplib,os
from bs4 import BeautifulSoup

URL = "https://www.emag.ro/prelata-sintetica-outsunn-verde-300x100-cm-844-204/pd/DWWTD8BBM/?ref=keep_shopping_for_3_6&provider=rec&recid=rec_65_2a1ccc7cfc5cd893c802c4cdb42d561dfe7c5a1c33887d75ade36b34b5786bc6_1699046814&scenario_ID=65"

desired_price = 200.00

MAIL = os.environ["mail"]
PASSWORD = os.environ["password"]

response = requests.get(url=URL)

soup = BeautifulSoup(response.text, "html.parser")
price = soup.find(name="p", class_="product-new-price")
price_text = price.text
price_parts = price_text.split(',')
price_final = price_parts[0] + '.' + price_parts[1].split('<')[0]
price_final = float(price_final.replace("Lei", "").strip())
print(price_final)
if price_final <= desired_price:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user= MAIL, password= PASSWORD)
        SUBJECT = " Emag Price Notifier"
        TEXT = f"Price Alert! The price has dropped. Current value: {price_final}"
        connection.sendmail(
            from_addr= MAIL,
            to_addrs= MAIL,
            msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        )


