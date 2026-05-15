# Painel onde professor e aluno recebem os avisos da coordenação
import streamlit as st
from data.avisos_store import avisos_para

st.title('Avisos')
st.caption('Comunicados enviados pela coordenação da Escola Estadual Machado de Assis')

st.divider()

# Descobre quem está logado para filtrar os avisos do público certo
papel = st.session_state.get('papel', 'aluno')
avisos = avisos_para(papel)

if not avisos:
    st.info('Nenhum aviso da coordenação no momento.')
else:
    # Cada aviso é exibido como um cartão expansível, do mais recente ao mais antigo
    for aviso in avisos:
        with st.container(border=True):
            st.markdown(f"### {aviso['titulo']}")
            st.caption(f"{aviso['data']}  ·  Para: {aviso['publico']}")
            st.write(aviso['mensagem'])
