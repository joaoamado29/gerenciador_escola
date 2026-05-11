import streamlit as st
from pages.navigation import nav_render
from ui.styles import load_css

st.set_page_config(initial_sidebar_state="collapsed")
load_css()

def main() -> None:
    nav_render()

if __name__ == "__main__":
    main()
