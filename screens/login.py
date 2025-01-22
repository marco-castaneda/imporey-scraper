import os
import streamlit as st # type: ignore


def login_page(supabase):
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


def logout(supabase):
    supabase.auth.sign_out()  # Cierra sesión en Supabase
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.success("Has cerrado sesión.")
    st.rerun()