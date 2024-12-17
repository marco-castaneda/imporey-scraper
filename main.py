import requests
from bs4 import BeautifulSoup
import streamlit as st # type: ignore
import pandas as pd
import openpyxl
from io import BytesIO
from tempfile import NamedTemporaryFile
from openpyxl.styles import Color, PatternFill
import json
import decimal
from itertools import cycle
import random
import time
import os
from dotenv import load_dotenv # type: ignore
from firecrawl import FirecrawlApp  # type: ignore
import re

from scrappers import (
    check_amazon, 
    check_liverpool,
    check_mercadolibre, 
    check_walmart,
    check_home_depot
)



def chunk_list(lst, chunk_size):
    """Splits a list into chunks of a specific size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]





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

def main():
    # mas de un archivo
    # descarga del zip creado de facturapi
    st.title("Marketplace Product Status Extractor")

    dataset = st.file_uploader("Upload Excel file (.xlsx)", type=['xlsx'])
    results = {}

    if dataset is not None:
        wb = openpyxl.load_workbook(dataset, read_only=True)
        st.info(f"File uploaded: {dataset.name}")

        ws = wb.active

        ###
        # End Result Excel Variables
        result_wb = openpyxl.Workbook()
        result_ws = result_wb.active

        keys = [
            "Marketplace", "Codigo", "Descripcion", "Link", "Estatus",
            "Precio Regular", "Precio Promoción", "Calificación", "# Reseñas"
        ]
        result_row_num = 1

        for col_num, column_title in enumerate(keys, 1):
            cell = result_ws.cell(row=result_row_num, column=col_num) # type: ignore
            cell.value = column_title

        st.write("Procesando archivo...")

        i = 0
        for row in ws.iter_rows(min_row=2, values_only=True):# type: ignore
            if row[0] is None:
                continue
            result_row_num += 1

            marketplace = row[0]
            product_code = row[1]
            product_name = row[2]
            link = row[3]

            result = ""
            price = "-"
            rating = "-"
            reviews = "-"
            promotion_price = "-"
            if marketplace == 'Amazon':
                result, price, promotion_price, rating, reviews = check_amazon(
                    link)
            elif marketplace == 'ML':
                result, price, promotion_price, rating, reviews = check_mercadolibre(
                    link)

            elif marketplace == 'Liverpool':
                result, price, promotion_price, rating, reviews = check_liverpool(
                    link)
            elif marketplace == 'Walmart':
                result, price, promotion_price, rating, reviews = check_walmart(link)# type: ignore
            elif marketplace == 'HomeDepot':
                result, price, promotion_price, rating, reviews = check_home_depot(
                    link)
            elif marketplace == 'Coppel':
                result, price, promotion_price, rating, reviews = check_coppel(
                    link)

            row = [
                marketplace, product_code, product_name, link, result, price,
                promotion_price, rating, reviews
            ]

            for col_num, cell_value in enumerate(row, 1):
                cell = result_ws.cell(row=result_row_num, column=col_num)# type: ignore
                cell.value = cell_value
            i += 1

        st.write("Terminando de procesar archivo...")
        st.write("Se procesaron ", i, " productos.")
        for e_column in result_ws['E']:# type: ignore
            if e_column.value == "ACTIVO":
                e_column.fill = PatternFill(start_color='38B856',
                                            end_color='38B856',
                                            fill_type='solid')
            if e_column.value == "INACTIVO":
                e_column.fill = PatternFill(start_color='d30000',
                                            end_color='d30000',
                                            fill_type='solid')
            if e_column.value in [
                    "PAGINA NO ENCONTRADA", "Failed to fetch the page"
            ]:
                e_column.fill = PatternFill(start_color='808080',
                                            end_color='808080',
                                            fill_type='solid')
        with NamedTemporaryFile() as tmp:
            result_wb.save(tmp.name)
            data = BytesIO(tmp.read())

        st.subheader("Resultados")
        st.download_button("Descargar Archivo",
                           data=data,
                           mime='xlsx',
                           file_name="resultados.xlsx")


if __name__ == "__main__":
    main()
