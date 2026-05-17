# Ponto de entrada do app Streamlit
import streamlit as st
from dotenv import load_dotenv

from auth import exigir_autenticacao
from pages.navigation import nav_admin, nav_aluno, nav_professor
from ui.styles import load_css

# Carrega variáveis do .env (inclui ADMIN_SENHA_INICIAL usada no seed)
load_dotenv()

# Configura a página e carrega o CSS customizado
st.set_page_config(initial_sidebar_state="collapsed")
load_css()


# Roteia para a navegação correta conforme o papel do usuário logado
def _rotear_por_papel() -> None:
    papel = st.session_state.get("papel")
    if papel == "admin":
        nav_admin()
    elif papel == "professor":
        nav_professor()
    elif papel == "aluno":
        nav_aluno()
    else:
        st.error("Papel de usuário desconhecido. Faça login novamente.")


def main() -> None:
    # Gate: bloqueia a navegação até o usuário logar e trocar a senha inicial
    if not exigir_autenticacao():
        return
    _rotear_por_papel()


if __name__ == "__main__":
    main()
