import streamlit as st

def btn_sidebar():
    if st.sidebar.button('Início', width="stretch", type="tertiary"):
        st.switch_page("app.py")
    if st.sidebar.button('Frequencia', width="stretch", type="tertiary"):
        st.switch_page("pages/frequencia.py")
    if st.sidebar.button('Boletim', width="stretch", type="tertiary"):
        st.switch_page("pages/boletim.py")
    if st.sidebar.button('Calendario', width="stretch", type="tertiary"):
        st.switch_page("pages/calendario.py")
    if st.sidebar.button('Avisos', width="stretch", type="tertiary"):
        st.switch_page("pages/avisos.py")
