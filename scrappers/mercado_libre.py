import requests
from bs4 import BeautifulSoup

def check_mercadolibre(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            if "publicación pausada" in response.text.lower():
                return "INACTIVO", 0, 0, "-", "-"
            else:
                price = soup.find("span",
                                  class_="andes-money-amount__fraction")
                promotion_price = soup.find(
                    "span", class_="andes-money-amount__fraction")
                price_arr = soup.find_all(
                    "span", class_="andes-money-amount__fraction")
                try:
                    list_price = price_arr[0]
                    promotion_price = None
                    if len(price_arr) > 1:
                        promotion_price = price_arr[1]
                except IndexError:
                    return "Información de precio no encontrado", 0, 0, "-", "-"

                rating = soup.find("span", "ui-pdp-review__rating")
                review = soup.find(
                    "p",
                    class_="ui-review-ui-review-capability__rating__label")
                return ("ACTIVO",
                        (list_price.text if price is not None else "-"),
                        (promotion_price.text
                         if promotion_price is not None else "-"),
                        (rating.text if rating is not None else "-"),
                        (review.text if review is not None else "-"))
        else:
            return "PAGINA NO ENCONTRADA", 0, 0, "-", "-"
    except requests.RequestException as e:
        print(e)
        return "Error al intentar acceder a la pag", 0, 0, "-", "-"