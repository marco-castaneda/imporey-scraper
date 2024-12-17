import requests
from bs4 import BeautifulSoup

def check_coppel(url):
    #url must be https://www.coppel.com.mx/$product
    try:
        response = requests.get(url)
        if response.status_code == 200:
            discounted_price = None
            original_price = None
            soup = BeautifulSoup(response.text, 'html.parser')

            discounted_price = soup.find('h2', {'data-testid': 'pdp_discounted_price'})

            if discounted_price is not None:
                original_price = soup.find('p', {'data-testid': 'pdp_price'})
            else:
                original_price = soup.find('h2', {'data-testid': 'pdp_price'})


            if discounted_price is None and original_price is None:
                return "PAGINA NO ENCONTRADA", "-", "-", "-", "-"

            return "ACTIVO", (original_price.text if original_price is not None else "-"), (discounted_price.text if discounted_price is not None else "-"),  "-", "-"
        else:
            return "INACTIVO", "-", "-", "-", "-"
    except requests.RequestException as e:
            return "PAGINA NO ENCONTRADA", "-", "-", "-", "-"
