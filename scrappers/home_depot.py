
import requests

def check_home_depot(url):
    try:

        last_part = url.split("/")[-1]
        last_value = last_part.split("-")[-1]
        home_depot_request = f'https://www.homedepot.com.mx/search/resources/api/v2/products?langId=-5&storeId=10351&contractId=4000000000000000003&langId=-5&partNumber={last_value}&physicalStoreId=8702'
        response = requests.get(home_depot_request)
        data = response.json()
        promotion_price = None
        rating = None
        review = None
        list_price = None
        status = "INACTIVO"
        base_data = data["contents"][0]
        for price_pos in base_data["price"]:
            if price_pos["usage"] == "Offer":
                promotion_price = price_pos["value"]
            if price_pos["usage"] == "Display":
                list_price = price_pos["value"]
        if "x_ratings.total_reviews" in base_data:
            review = base_data["x_ratings.total_reviews"]
        if "x_ratings.rating" in base_data:
            rating = base_data["x_ratings.rating"]
        product_id = base_data["id"]
        status_request = f'https://www.homedepot.com.mx/wcs/resources/store/10351/inventoryavailability/{product_id}?&langId=-5&onlineStoreId=10351&search=2&physicalStoreId=12605'
        response = requests.get(status_request)
        availabilty_data = response.json()
        if availabilty_data["InventoryAvailability"][0][
                "inventoryStatus"] == "Available":
            status = "ACTIVO"

        return (status, (list_price if list_price is not None else "-"),
                (promotion_price if promotion_price is not None else "-"),
                (rating if rating is not None else "-"),
                (review if review is not None else "-"))
    except requests.RequestException:
        return "Failed to fetch the page"