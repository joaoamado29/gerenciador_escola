# Página do professor: filtra por disciplina, dia e turno e mostra onde dá aula
import streamlit as st

from data.grade_store import (
    DIAS,
    DISCIPLINAS,
    TURNOS,
    aulas_do_professor,
)

# TODO: substituir pela disciplina vinda do login quando houver autenticação
DISCIPLINA_PADRAO = 'Matemática'

st.title('Grade Horária')
st.caption('Selecione disciplina, dia e turno para ver suas aulas')

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    disciplina = st.selectbox(
        'Disciplina:', DISCIPLINAS, index=DISCIPLINAS.index(DISCIPLINA_PADRAO)
    )
with col2:
    dia = st.selectbox('Dia da semana:', DIAS)
with col3:
    turno = st.selectbox('Turno:', TURNOS)

st.divider()

aulas = aulas_do_professor(disciplina, dia, turno)

if not aulas:
    st.info(f'Nenhuma aula de {disciplina} em {dia} ({turno}).')
else:
    linhas = [
        {
            'Aula': f"{a['indice_aula']}ª",
            'Horário': f"{a['hora_inicio']} – {a['hora_fim']}",
            'Turma': a['turma'],
        }
        for a in aulas
    ]
    st.dataframe(linhas, hide_index=True, width='stretch')
