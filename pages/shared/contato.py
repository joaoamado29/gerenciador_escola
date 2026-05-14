# Página de contato (somente leitura) com as informações da escola
import streamlit as st

st.title('Contato')
st.caption('Entre em contato com a Escola Estadual Machado de Assis')

st.divider()

# Endereço e horário (lado a lado em telas maiores)
col1, col2 = st.columns(2)

with col1:
    st.subheader('Endereço')
    st.markdown(
        'Av. Washington Soares\n\n'
        'Bairro Edson Queiroz\n\n'
        'Fortaleza – CE\n\n'
        'CEP: 01234-567'
    )

with col2:
    st.subheader('Horário de Atendimento')
    st.markdown(
        'Segunda a Sexta: **07h00 – 18h00**\n\n'
        'Sábado: **08h00 – 12h00**\n\n'
        'Domingo: *fechado*'
    )

st.divider()

# Contatos diretos
st.subheader('Fale Conosco')

col3, col4 = st.columns(2)

with col3:
    st.markdown('**Secretaria**')
    st.markdown('Telefone: (85) 0000-0000')
    st.markdown('E-mail: secretaria@machadodeassis.edu.br')

with col4:
    st.markdown('**Coordenação Pedagógica**')
    st.markdown('Telefone: (85) 0000-0000')
    st.markdown('E-mail: coordenacao@machadodeassis.edu.br')

st.divider()

# Redes sociais e canais adicionais
st.subheader('Redes Sociais')
st.markdown(
    '- Instagram: @escolamachadodeassis\n'
    '- Facebook: /escolamachadodeassis\n'
    '- WhatsApp: (85) 9876-5432\n'
    '- Site: www.machadodeassis.edu.br'
)
