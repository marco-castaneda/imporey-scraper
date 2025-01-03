import streamlit as st # type: ignore
from screens import login_page, scrape_page
from supabase import create_client, Client
import os

def main():
    return None

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


if __name__ == "__main__":
    main()
