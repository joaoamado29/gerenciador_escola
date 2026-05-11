import streamlit as st

def nav_render():
    pages = {
        "Aluno": [
            st.Page("pages/inicio.py", title="Início", default=True),
            st.Page("pages/boletim.py", title="Boletim"),
            st.Page("pages/frenquencia.py", title="Frequência"),
        ],
        "Importante": [
            st.Page("pages/avisos.py", title="Avisos"),
            st.Page("pages/contato.py", title="Contato")
        ],
        "Horários": [
            st.Page("pages/calendario.py", title="Calendário"),
            st.Page("pages/horarios.py", title="Horário de Aula"),
        ],
    }

    pg = st.navigation(pages, position="top")
    pg.run()
