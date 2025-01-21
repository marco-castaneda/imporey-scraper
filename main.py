import streamlit as st  # type: ignore
from screens import login_page, scrape_page
from supabase import create_client, Client
import os
from data import make_report  # type: ignore
import schedule
import time
import threading
import pytz
from datetime import datetime

def supabase_client():
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if SUPABASE_URL is not None and SUPABASE_KEY is not None:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        scrape_page(supabase=supabase_client())
    else:
        login_page(supabase=supabase_client())

    
    if st.button("Make report"):
        run_report()

def run_report():
    print("Making report...")
    #make_report()
    
local_tz = pytz.timezone("America/Monterrey")
hour = "13:10"
def run_schedule():
    while True:
        now = datetime.now(local_tz).strftime("%H:%M")
        print("now")
        print(now)
        if now == hour:
            run_report()
        time.sleep(60)

#schedule.every().day.at(hour).do(run_report)
schedule.every(10).minutes.do(run_report)

thread = threading.Thread(target=run_schedule, daemon=True)
thread.start()

if __name__ == "__main__":
    main()
