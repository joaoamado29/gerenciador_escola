import streamlit as st
from data.turmas import selecionar_turma, alunos_da_turma

BIMESTRES = ['1º Bimestre', '2º Bimestre', '3º Bimestre', '4º Bimestre']


def selecionar_aluno(turma):
    alunos = alunos_da_turma(turma)
    if not alunos:
        st.warning('Nenhum aluno cadastrado para esta turma.')
        return None
    return st.selectbox('Aluno:', alunos)


def lancar_notas(turma, aluno, bimestre):
    key_prefix = f'nota_{turma}_{aluno}_{bimestre}'

    with st.form(key=f'form_{key_prefix}'):
        col1, col2 = st.columns(2)
        with col1:
            parcial = st.number_input(
                'Nota Parcial',
                min_value=0.0,
                max_value=10.0,
                step=0.1,
                value=None,
                placeholder='0,0 – 10,0',
                key=f'{key_prefix}_parcial',
            )
        with col2:
            bimestral = st.number_input(
                'Nota Bimestral',
                min_value=0.0,
                max_value=10.0,
                step=0.1,
                value=None,
                placeholder='0,0 – 10,0',
                key=f'{key_prefix}_bimestral',
            )

        enviado = st.form_submit_button('Enviar Média', use_container_width=True)

    if enviado:
        if parcial is None or bimestral is None:
            st.error('Preencha as duas notas antes de enviar.')
            return
        media = (parcial + bimestral) / 2
        st.success(f'Média de {aluno} no {bimestre}: **{media:.2f}**')


st.title('Gerenciar Notas')

turma = selecionar_turma()
st.caption(f'Turma: {turma[0]} • {turma[1]} • {turma[2]}')

aluno = selecionar_aluno(turma)
if aluno:
    bimestre = st.selectbox('Bimestre:', BIMESTRES)
    st.divider()
    lancar_notas(turma, aluno, bimestre)
