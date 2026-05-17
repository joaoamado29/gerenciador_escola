# Página da conta do usuário logado: dados básicos + troca de senha + logout.
import streamlit as st

from auth import logout, tela_trocar_senha, usuario_logado

if not usuario_logado():
    st.error("Você precisa estar logado para acessar esta página.")
    st.stop()

st.title("Minha conta")

col1, col2 = st.columns(2)
with col1:
    st.metric("Matrícula", st.session_state.get("matricula", "—"))
with col2:
    st.metric("Papel", str(st.session_state.get("papel", "—")).capitalize())

st.markdown(f"**Nome:** {st.session_state.get('nome', '—')}")

st.divider()

tela_trocar_senha(obrigatoria=False)

st.divider()
if st.button("Sair", type="secondary"):
    logout()
    st.rerun()
