import streamlit as st  # type: ignore
from screens import login_page, scrape_page
from supabase import create_client, Client
import os
import schedule  # type: ignore
import threading
import time
from data import extrac_from_db, dowload_results_file
from helpers import make_report  # type: ignore


def supabase_client():
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if SUPABASE_URL is not None and SUPABASE_KEY is not None:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase
    return None

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        scrape_page(supabase=supabase_client)
    else:
        login_page(supabase=supabase_client)

    
    if st.button("Make report"):
        run_report()

def run_report():
    #extrac_from_db(marketplace="All", supabase=supabase_client())
    print("Making report...")
    make_report()
    

""" def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every(10).minutes.do(run_report)

thread = threading.Thread(target=run_schedule, daemon=True)
thread.start() """

if __name__ == "__main__":
    main()
