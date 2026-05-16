# Página inicial compartilhada (exibe o nome da escola)
import streamlit as st
from data.avisos_store import avisos_para

st.title('Escola Estadual Machado de Assis')

st.divider()

# Prévia do aviso mais recente da coordenação
st.subheader('Último aviso')
papel = st.session_state.get('papel', 'aluno')
avisos = avisos_para(papel)

if not avisos:
    st.info('Nenhum aviso da coordenação no momento.')
else:
    recente = avisos[0]
    with st.container(border=True):
        st.markdown(f"**{recente['titulo']}**")
        st.caption(f"{recente['data']}  ·  Para: {recente['publico']}")
        st.write(recente['mensagem'])
    if st.button('Ver todos os avisos'):
        st.switch_page('pages/shared/avisos.py')
