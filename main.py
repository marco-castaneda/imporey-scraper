import streamlit as st # type: ignore
from screens import login_page, scrape_page

def main():
    return None


if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    scrape_page()
else:
    login_page()


if __name__ == "__main__":
    main()
