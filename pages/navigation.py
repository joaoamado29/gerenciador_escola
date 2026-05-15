# Define as barras de navegação superiores para cada tipo de usuário
import streamlit as st


# Navegação para o aluno
def nav_aluno():
    # Identifica o tipo de usuário para as páginas compartilhadas (ex.: Avisos)
    st.session_state['papel'] = 'aluno'
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
    }

    # Renderiza o menu no topo e executa a página escolhida
    pg = st.navigation(pages, position="top")
    pg.run()


# Navegação para o professor
def nav_professor():
    st.session_state['papel'] = 'professor'
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
    }

    pg = st.navigation(pages, position="top")
    pg.run()

# Navegação para o administrador
def nav_admin():
    st.session_state['papel'] = 'admin'
    pages = {
        "Admin": [
            st.Page("pages/shared/inicio.py", title="Início", default=True),
            st.Page("pages/admin/gerenciar_usuarios.py", title="Gerenciar Usuários"),
            st.Page("pages/admin/dashboards.py", title="Dashboards"),
            st.Page("pages/admin/relatorios.py", title="Relatórios"),
            st.Page("pages/admin/enviar_mensagem.py", title="Enviar Aviso"),
        ],
        "Importante": [
            st.Page("pages/shared/avisos.py", title="Avisos"),
            st.Page("pages/shared/contato.py", title="Contato")
        ],
        "Horários": [
            st.Page("pages/shared/calendario.py", title="Calendário"),
            st.Page("pages/professor/grade_horaria.py", title="Grade Horária"),
        ],
    }

    pg = st.navigation(pages, position="top")
    pg.run()
