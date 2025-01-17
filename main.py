import streamlit as st  # type: ignore
from screens import login_page, scrape_page
from supabase import create_client, Client
import os
import schedule  # type: ignore
import threading
import time

def main():
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if SUPABASE_URL is not None and SUPABASE_KEY is not None:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        scrape_page(supabase=supabase)
    else:
        login_page(supabase=supabase)

def tarea_periodica():
    print("Resultado de la tarea periódica")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Configuración de la tarea periódica
schedule.every(1).minutes.do(tarea_periodica)

# Iniciar un hilo separado para ejecutar las tareas programadas
thread = threading.Thread(target=run_schedule, daemon=True)
thread.start()

if __name__ == "__main__":
    main()
