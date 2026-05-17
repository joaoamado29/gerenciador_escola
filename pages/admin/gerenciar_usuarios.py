# Página do administrador para criar e listar usuários (professores e alunos).
from datetime import datetime

import streamlit as st

from auth import validar_forca_senha
from data.usuarios_store import (
    criar_usuario,
    gerar_matricula_aluno,
    gerar_senha_inicial_aluno,
    listar_por_papel,
)

# Defesa em profundidade: só admin pode ver esta página
if st.session_state.get("papel") != "admin":
    st.error("Acesso restrito ao administrador.")
    st.stop()

st.title("Gerenciar Usuários")

aba_prof, aba_aluno, aba_lista = st.tabs(
    ["Cadastrar Professor", "Cadastrar Aluno", "Usuários Cadastrados"]
)

# ---- Cadastro de professor ---------------------------------------------------
with aba_prof:
    st.subheader("Novo Professor")
    st.caption(
        "Matrícula gerada automaticamente (6 dígitos). "
        "O professor precisará trocar a senha no primeiro acesso."
    )
    with st.form("form_prof", clear_on_submit=True):
        nome_prof = st.text_input("Nome completo")
        senha_prof = st.text_input(
            "Senha inicial", type="password",
            help="Mínimo 8 caracteres, com letra e número."
        )
        enviar_prof = st.form_submit_button("Cadastrar", type="primary")

    if enviar_prof:
        ok, msg = validar_forca_senha(senha_prof)
        if not nome_prof.strip():
            st.error("Informe o nome do professor.")
        elif not ok:
            st.error(msg)
        else:
            try:
                criado = criar_usuario(
                    papel="professor",
                    nome=nome_prof,
                    senha=senha_prof,
                    deve_trocar_senha=True,
                )
                st.success(
                    f"Professor criado. Matrícula: **{criado['matricula']}**"
                )
            except (ValueError, RuntimeError) as e:
                st.error(f"Erro ao criar professor: {e}")

# ---- Cadastro de aluno -------------------------------------------------------
with aba_aluno:
    st.subheader("Novo Aluno")
    st.caption(
        "Matrícula = ano + 8 dígitos sorteados. "
        "Senha inicial = ano + 2 últimos dígitos da matrícula; "
        "trocada no primeiro acesso."
    )
    ano_atual = datetime.utcnow().year
    with st.form("form_aluno", clear_on_submit=True):
        nome_aluno = st.text_input("Nome completo")
        ano = st.number_input(
            "Ano de matrícula",
            min_value=2000, max_value=ano_atual + 1,
            value=ano_atual, step=1,
        )
        enviar_aluno = st.form_submit_button("Cadastrar", type="primary")

    if enviar_aluno:
        if not nome_aluno.strip():
            st.error("Informe o nome do aluno.")
        else:
            try:
                matricula = gerar_matricula_aluno(int(ano))
                senha_inicial = gerar_senha_inicial_aluno(int(ano), matricula)
                criado = criar_usuario(
                    papel="aluno",
                    nome=nome_aluno,
                    senha=senha_inicial,
                    matricula=matricula,
                    ano_matricula=int(ano),
                    deve_trocar_senha=True,
                )
                st.success(
                    f"Aluno criado. Matrícula: **{criado['matricula']}**  ·  "
                    f"Senha inicial: **{senha_inicial}** "
                    "(anote — será trocada no 1º acesso)"
                )
            except (ValueError, RuntimeError) as e:
                st.error(f"Erro ao criar aluno: {e}")

# ---- Listagem ----------------------------------------------------------------
with aba_lista:
    st.subheader("Usuários cadastrados")
    for papel in ("admin", "professor", "aluno"):
        with st.expander(f"{papel.capitalize()}s", expanded=(papel != "aluno")):
            usuarios = listar_por_papel(papel)
            if not usuarios:
                st.caption("Nenhum usuário cadastrado.")
                continue
            for u in usuarios:
                pendente = " · *senha pendente de troca*" if u.get("deve_trocar_senha") else ""
                st.markdown(
                    f"- **{u['matricula']}** — {u['nome']}{pendente}"
                )
