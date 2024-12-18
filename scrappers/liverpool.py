
import requests
from bs4 import BeautifulSoup
import decimal
from helpers import check_url  # type: ignore
import json


def check_liverpool(url):
    url = check_url(url)
    try:
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.google.com/",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find("script", id="__NEXT_DATA__")
            json_object = json.loads(script_tag.text) # type: ignore
            discount_price = 0
            regular_price = 0
            if json_object["query"]["data"]["mainContent"]["records"][0][
                    "allMeta"]["variants"][0]["prices"][
                        "promoPrice"] is not None or decimal.Decimal(
                            json_object["query"]["data"]["mainContent"]
                            ["records"][0]["allMeta"]["variants"][0]["prices"]
                            ["promoPrice"]) > 0:
                discount_price = json_object["query"]["data"]["mainContent"][
                    "records"][0]["allMeta"]["variants"][0]["prices"][
                        "promoPrice"]

            regular_price = json_object["query"]["data"]["mainContent"][
                "records"][0]["allMeta"]["variants"][0]["prices"]["listPrice"]

            return ("ACTIVO",
                    (regular_price if regular_price is not None else "-"),
                    (discount_price if discount_price is not None else "-"),
                    "-", "-")
        else:
            return "INACTIVO", 0, 0, "-", "-"

    except requests.RequestException as e:
        return "PAGINA NO ENCONTRADA", 0, 0, "-", "-"
