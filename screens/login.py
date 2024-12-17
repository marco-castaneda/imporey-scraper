import os
import streamlit as st # type: ignore
from supabase import create_client, Client


SUPABASE_URL = os.environ['SUPABASE_URL']
SUPABASE_KEY = os.environ['SUPABASE_KEY']

if SUPABASE_URL is not None and SUPABASE_KEY is not None:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def login_page():
    st.title("Inicio de Sesión")
    st.write("Por favor, inicia sesión para continuar.")
    
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if user:
                st.success("Inicio de sesión exitoso")
                st.session_state["authenticated"] = True
                st.rerun()
        except Exception as e:
            st.error(f"Error de autenticación: {str(e)}")


def logout():
    supabase.auth.sign_out()  # Cierra sesión en Supabase
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.success("Has cerrado sesión.")
    st.rerun()