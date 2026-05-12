# Carrega o CSS customizado dentro do app Streamlit
from pathlib import Path
import streamlit as st


# Lê o arquivo .css e injeta o conteúdo na página via <style>
def load_css(path: str = "assets/styles.css"):
    css = Path(path).read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
