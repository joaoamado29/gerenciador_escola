# Define as barras de navegação superiores para cada tipo de usuário.
# O 'papel' vem do auth.py (sessão autenticada) e NÃO deve ser sobrescrito aqui.
import streamlit as st

from auth import logout


# Botão de logout fixo na sidebar (exibido junto com qualquer navegação)
def _sidebar_logout() -> None:
    nome = st.session_state.get("nome", "")
    matricula = st.session_state.get("matricula", "")
    if nome:
        st.sidebar.caption(f"Logado como **{nome}** ({matricula})")
    if st.sidebar.button("Sair", width="stretch", type="secondary"):
        logout()
        st.rerun()


# Navegação para o aluno
def nav_aluno():
    _sidebar_logout()
    # Agrupa as páginas em seções exibidas no menu superior
    pages = {
        "Aluno": [
            st.Page("pages/shared/inicio.py", title="Início", default=True),
            st.Page("pages/aluno/boletim.py", title="Boletim"),
            st.Page("pages/aluno/frequencia.py", title="Frequência"),
        ],
        "Importante": [
            st.Page("pages/shared/avisos.py", title="Avisos"),
            st.Page("pages/shared/contato.py", title="Contato")
        ],
        "Horários": [
            st.Page("pages/shared/calendario.py", title="Calendário"),
            st.Page("pages/aluno/horarios.py", title="Horário de Aula"),
        ],
        "Conta": [
            st.Page("pages/shared/conta.py", title="Minha Conta"),
        ],
    }

    # Renderiza o menu no topo e executa a página escolhida
    pg = st.navigation(pages, position="top")
    pg.run()


# Navegação para o professor
def nav_professor():
    _sidebar_logout()
    pages = {
        "Professor": [
            st.Page("pages/shared/inicio.py", title="Início", default=True),
            st.Page("pages/professor/gerenciar_notas.py", title="Gerenciar Notas"),
            st.Page("pages/professor/gerenciar_frequencia.py", title="Gerenciar Frequência"),
        ],
        "Importante": [
            st.Page("pages/shared/avisos.py", title="Avisos"),
            st.Page("pages/shared/contato.py", title="Contato")
        ],
        "Horários": [
            st.Page("pages/shared/calendario.py", title="Calendário"),
            st.Page("pages/professor/grade_horaria.py", title="Grade Horária"),
        ],
        "Conta": [
            st.Page("pages/shared/conta.py", title="Minha Conta"),
        ],
    }

    pg = st.navigation(pages, position="top")
    pg.run()


# Navegação para o administrador
def nav_admin():
    _sidebar_logout()
    pages = {
        "Admin": [
            st.Page("pages/shared/inicio.py", title="Início", default=True),
            st.Page("pages/admin/gerenciar_usuarios.py", title="Gerenciar Usuários"),
            st.Page("pages/admin/dashboards.py", title="Dashboards"),
            st.Page("pages/admin/relatorios.py", title="Relatórios"),
        ],
        "Importante": [
            st.Page("pages/shared/avisos.py", title="Avisos"),
            st.Page("pages/shared/contato.py", title="Contato"),
            st.Page("pages/admin/enviar_mensagem.py", title="Enviar Aviso"),
        ],
        "Horários": [
            st.Page("pages/shared/calendario.py", title="Calendário"),
            st.Page("pages/admin/grade_horaria.py", title="Grade Horária"),
        ],
        "Conta": [
            st.Page("pages/shared/conta.py", title="Minha Conta"),
        ],
    }

    pg = st.navigation(pages, position="top")
    pg.run()
