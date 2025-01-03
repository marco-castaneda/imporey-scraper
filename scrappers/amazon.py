
import os
import time
import random
import requests
from bs4 import BeautifulSoup
from firecrawl import FirecrawlApp  # type: ignore
import streamlit as st # type: ignore
import os

def check_amazon(url):
    try:

        if not url.startswith("https"):
            url = "https://www.amazon.com.mx/gp/product/" + url

        current_price = None
        original_price = None
        rating = None
        reviews = None
        inactive = False
        no_available = None
        no_offers = None

        app = FirecrawlApp(api_key=os.getenv["FC_API_KEY"])

        time.sleep(random.uniform(1, 4))

        response = app.scrape_url(url=url, params={
            'formats': [ 'html' ],
        })

        soup = BeautifulSoup(response['html'], 'html.parser')

        if soup.find('div', id='averageCustomerReviews') is not None:
            rating_span = soup.find('div', id='averageCustomerReviews').find('a', class_='a-popover-trigger a-declarative').find('span', class_='a-size-base a-color-base')# type: ignore
            rating = rating_span.text.strip() # type: ignore

        if soup.find('span', id='acrCustomerReviewText') is not None:
            reviews_span = soup.find('span', id='acrCustomerReviewText')
            reviews = reviews_span.text.split()[0] if reviews_span else None
        if soup.find('div', class_="a-section a-spacing-small a-text-center") is not None and soup.find('span', string="No disponible por el momento.") is not None:
            no_available = soup.find('div', class_="a-section a-spacing-small a-text-center").find('span', string="No disponible por el momento.") # type: ignore

        if soup.find('span', string="No hay ofertas destacadas disponibles") is not None:
            no_offers = soup.find('span', string="No hay ofertas destacadas disponibles")

        if no_offers or no_available:
            return "INACTIVO", "-", "-", rating if rating is not None else "-", reviews if reviews is not None else "-"
        else:
            if not inactive:
                if soup.find('span', class_='a-price aok-align-center') is not None:
                    current_price_span = soup.find('span', class_='a-price aok-align-center').find('span', class_='a-offscreen') # type: ignore
                    current_price = current_price_span.text.strip() if current_price_span else None

                if soup.find('span', class_='a-size-small a-color-secondary aok-align-center basisPrice') is not None:
                    original_price_span = soup.find('span', class_='a-size-small a-color-secondary aok-align-center basisPrice').find('span', class_='a-price a-text-price').find('span', class_='a-offscreen') # type: ignore
                    original_price = original_price_span.text.strip() if original_price_span else None
                return "ACTIVO", current_price, original_price, rating if rating is not None else "-", reviews if reviews is not None else "-"
            else:
                return "INACTIVO", "-", "-", rating if rating is not None else "-", reviews if reviews is not None else "-"


    except requests.RequestException as e:
        return "PAGINA NO ENCONTRADA", 0, 0, "-", "-"