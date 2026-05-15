# Página da coordenação para publicar e gerenciar os avisos
import streamlit as st
from data.avisos_store import PUBLICOS, adicionar_aviso, listar_avisos, remover_aviso

st.title('Enviar Aviso')
st.caption('Publique comunicados para os professores e alunos')

st.divider()

# Formulário de publicação de um novo aviso
with st.form('novo_aviso', clear_on_submit=True):
    titulo = st.text_input('Título', max_chars=80)
    mensagem = st.text_area('Mensagem', max_chars=350)
    publico = st.selectbox('Enviar para', PUBLICOS)
    enviar = st.form_submit_button('Publicar aviso')

    if enviar:
        if titulo.strip() and mensagem.strip():
            adicionar_aviso(titulo.strip(), mensagem.strip(), publico)
            st.success('Aviso publicado!')
        else:
            st.error('Preencha o título e a mensagem antes de publicar.')

st.divider()

# Lista dos avisos já publicados, com opção de remover
st.subheader('Avisos publicados')

avisos = listar_avisos()
if not avisos:
    st.info('Nenhum aviso publicado ainda.')
else:
    for aviso in avisos:
        with st.container(border=True):
            st.markdown(f"**{aviso['titulo']}**")
            st.caption(f"{aviso['data']}  ·  Para: {aviso['publico']}")
            st.write(aviso['mensagem'])
            if st.button('Remover', key=f"remover_{aviso['id']}"):
                remover_aviso(aviso['id'])
                st.rerun()
