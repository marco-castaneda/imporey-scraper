import streamlit as st # type: ignore
import openpyxl
from io import BytesIO
from tempfile import NamedTemporaryFile
from openpyxl.styles import PatternFill

from data import extrac_from_db
from scrappers import (
    check_amazon, 
    check_liverpool,
    check_mercadolibre, 
    check_walmart,
    check_home_depot,
    check_coppel
)
from screens import logout

def scrape_page(supabase):
    if st.button("Cerrar Sesión"):
        logout(supabase=supabase)
    
    st.title("Marketplace Product Status Extractor")

    if st.button("Liverpool"):
        extrac_from_db(marketplace="Liverpool")

    dataset = st.file_uploader("Upload Excel file (.xlsx)", type=['xlsx'])

    if dataset is not None:
        build_excel_results(dataset=dataset)
        

def build_excel_results(dataset):

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
                        file_name=f"resultados_{marketplace}.xlsx")