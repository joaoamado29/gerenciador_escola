# Página do admin: edita a grade horária de cada turma
import streamlit as st

from data.grade_store import (
    DIAS,
    DISCIPLINAS,
    HORARIOS_AULAS,
    INTERVALO,
    TURMAS,
    TURNOS,
    atualizar_aula,
    atualizar_turno,
    grade_da_turma,
    turno_da_turma,
)

st.title('Grade Horária — Edição')
st.caption('Selecione uma turma para visualizar e alterar a grade')

st.divider()

col1, col2 = st.columns(2)
with col1:
    turma = st.selectbox('Turma:', TURMAS)
with col2:
    turno_atual = turno_da_turma(turma)
    novo_turno = st.selectbox(
        'Turno da turma:', TURNOS, index=TURNOS.index(turno_atual)
    )
    if novo_turno != turno_atual:
        atualizar_turno(turma, novo_turno)
        st.rerun()

st.divider()

grade = grade_da_turma(turma)
slots = HORARIOS_AULAS[turno_atual]
hora_intervalo = INTERVALO[turno_atual]

# Cabeçalho: coluna de horário + uma coluna por dia da semana
header = st.columns([1.2] + [1] * len(DIAS))
header[0].markdown('**Horário**')
for i, dia in enumerate(DIAS, start=1):
    header[i].markdown(f'**{dia}**')

# Linhas: 3 aulas, intervalo, mais 3 aulas
for indice in range(6):
    linha = st.columns([1.2] + [1] * len(DIAS))
    h_ini, h_fim = slots[indice]
    linha[0].markdown(f"{indice + 1}ª\n\n{h_ini} – {h_fim}")
    for col_dia, dia in enumerate(DIAS, start=1):
        valor_atual = grade[dia][indice]
        novo = linha[col_dia].selectbox(
            label=f'{dia}-{indice}',
            options=DISCIPLINAS,
            index=DISCIPLINAS.index(valor_atual),
            key=f'{turma}_{dia}_{indice}',
            label_visibility='collapsed',
        )
        if novo != valor_atual:
            atualizar_aula(turma, dia, indice, novo)
            st.rerun()

    if indice == 2:
        intervalo_linha = st.columns([1.2] + [1] * len(DIAS))
        intervalo_linha[0].markdown(
            f"Intervalo\n\n{hora_intervalo[0]} – {hora_intervalo[1]}"
        )
        for col_dia in range(1, len(DIAS) + 1):
            intervalo_linha[col_dia].markdown('—')
