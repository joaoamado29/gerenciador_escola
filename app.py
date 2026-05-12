import streamlit as st
from pages.navigation import nav_aluno, nav_professor, nav_admin
from ui.styles import load_css

st.set_page_config(initial_sidebar_state="collapsed")
load_css()

def main() -> None:
    nav_admin()

if __name__ == "__main__":
    main()
