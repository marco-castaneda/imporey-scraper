import os
import re
import time
import random
import requests
from dotenv import load_dotenv # type: ignore
from firecrawl import FirecrawlApp  # type: ignore

def check_walmart(url):
    try:
        load_dotenv()

        app = FirecrawlApp(api_key=os.getenv('FC_API_KEY'))

        time.sleep(random.uniform(1, 4))

        response = app.scrape_url(url=url, params={
            'formats': [ 'markdown' ],
        })

        current_price = None
        original_price = None
        stars = None
        reviews = None

        current_price_match = re.search(r'MXN$(\d+\.\d{2})', response["markdown"])
        current_price = f"${current_price_match.group(1)}" if current_price_match else None

        original_price_match = re.search(r'costaba \$(\d+\.\d{2})', response["markdown"])
        original_price = f"${original_price_match.group(1)}" if original_price_match else None

        stars_pattern = r"\((\d+\.\d+)\)(\d+\.\d+) estrellas de (\d+) reseñas"
        match_stars = re.search(stars_pattern, response["markdown"])

        if match_stars:
            stars = match_stars.group(1)
            reviews = match_stars.group(3)
        else:
            stars = None
            reviews = None

        if current_price is not None:
            return ("ACTIVO",
                    current_price,
                    (original_price
                        if original_price is not None else "-"),
                    (stars
                        if stars is not None else "-"),
                    (reviews
                        if reviews is not None else "-"))
        else:
            price_pattern = r"MXN\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)"
            match = re.search(price_pattern, response["markdown"])
            if match:
                current_price = f"${match.group(1)}"
                return ("ACTIVO",
                    current_price,
                    "-",
                     (stars
                        if stars is not None else "-"),
                    (reviews
                        if reviews is not None else "-"))
            else:
                return "INACTIVO", "-", "-", "-", "-"

    except requests.RequestException as e:
        return "PAGINA NO ENCONTRADA", 0, 0, "-", "-"

