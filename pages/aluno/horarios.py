# Página do aluno: mostra a grade do dia escolhido para a turma do aluno
import streamlit as st

from data.grade_store import (
    DIAS,
    INTERVALO,
    aulas_do_dia,
    turno_da_turma,
)

# TODO: substituir por turma vinda do login quando houver autenticação
TURMA_DO_ALUNO = '1º A'

st.title('Horário de Aula')
st.caption(f'Turma: {TURMA_DO_ALUNO}  ·  Turno: {turno_da_turma(TURMA_DO_ALUNO)}')

st.divider()

dia = st.selectbox('Dia da semana:', DIAS)

aulas = aulas_do_dia(TURMA_DO_ALUNO, dia)
turno = turno_da_turma(TURMA_DO_ALUNO)
hora_intervalo = INTERVALO[turno]

# Constrói a tabela do dia: 3 aulas + intervalo + 3 aulas
linhas = []
for i, aula in enumerate(aulas, start=1):
    linhas.append({
        'Aula': f'{i}ª',
        'Horário': f"{aula['hora_inicio']} – {aula['hora_fim']}",
        'Disciplina': aula['disciplina'],
    })
    if i == 3:
        linhas.append({
            'Aula': '—',
            'Horário': f'{hora_intervalo[0]} – {hora_intervalo[1]}',
            'Disciplina': 'Intervalo',
        })

st.dataframe(linhas, hide_index=True, width='stretch')
