# Página do professor para marcar a frequência dos alunos
import streamlit as st
from data.turmas import selecionar_turma, alunos_da_turma

# Opções de status que podem ser atribuídas a cada aluno
STATUS_FREQUENCIA = ['Presente', 'Falta', 'Falta Justificada']


# Renderiza a lista de alunos da turma com um radio de status para cada um
def marcar_frequencia(turma):
    alunos = alunos_da_turma(turma)
    if not alunos:
        st.warning('Nenhum aluno cadastrado para esta turma.')
        return {}

    st.subheader('Lista de alunos')

    # Cabeçalho da "tabela"
    with st.container(border=True):
        head_nome, head_status = st.columns([2, 3])
        head_nome.markdown('**Aluno**')
        head_status.markdown('**Frequência**')

    # Uma linha por aluno (nome à esquerda, opções de status à direita)
    registros = {}
    for aluno in alunos:
        with st.container(border=True):
            col_nome, col_status = st.columns([2, 3], vertical_alignment='center')
            with col_nome:
                st.markdown(f'**{aluno}**')
            with col_status:
                # key única por turma+aluno para não misturar estado entre turmas
                registros[aluno] = st.radio(
                    'Frequência',
                    STATUS_FREQUENCIA,
                    horizontal=True,
                    key=f'freq_{turma}_{aluno}',
                    label_visibility='collapsed',
                )
    return registros


st.title('Gerenciar Frequência')

# Seleção da turma e exibição dos alunos correspondentes
turma = selecionar_turma()
st.caption(f'Turma: {turma[0]} • {turma[1]} • {turma[2]}')

registros = marcar_frequencia(turma)

# Ao salvar, mostra um resumo em tabela (placeholder até ter persistência)
if registros and st.button('Salvar frequência'):
    st.success('Frequência registrada:')
    st.table([{'Aluno': a, 'Status': s} for a, s in registros.items()])
