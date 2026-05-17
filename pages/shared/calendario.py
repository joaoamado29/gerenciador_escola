# Página de calendário letivo compartilhada entre todos os usuários.
# Admin tem controles extras para cadastrar recessos e eventos.
import calendar as cal_lib
from datetime import date

import streamlit as st

from data.calendario_store import (
    DIAS_SEMANA,
    MESES,
    adicionar_evento,
    adicionar_recesso,
    listar_eventos,
    listar_recessos,
    remover_evento,
    remover_recesso,
    status_do_dia,
)

st.title('Calendário Letivo')
st.caption('Feriados, recessos, eventos, férias e período de recuperação')

hoje = date.today()

# Seletor de ano (ano anterior, atual e dois próximos) e mês
col_ano, col_mes = st.columns(2)
with col_ano:
    anos_opcoes = list(range(hoje.year - 1, hoje.year + 3))
    ano = st.selectbox('Ano', anos_opcoes, index=anos_opcoes.index(hoje.year))
with col_mes:
    mes_nome = st.selectbox('Mês', MESES, index=hoje.month - 1)
mes_num = MESES.index(mes_nome) + 1

# Legenda das cores (mesmas classes CSS usadas nas células)
st.markdown(
    """
    <div class="cal-legenda">
      <div class="item"><span class="box cal-fim_de_semana"></span>Sem aula (fim de semana / feriado / recesso)</div>
      <div class="item"><span class="box cal-evento"></span>Evento escolar</div>
      <div class="item"><span class="box cal-ferias"></span>Férias (Janeiro e Julho)</div>
      <div class="item"><span class="box cal-recuperacao"></span>Período de Recuperação</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Monta a matriz do mês com semanas começando na segunda-feira
semanas = cal_lib.Calendar(firstweekday=6).monthdatescalendar(ano, mes_num)

linhas = []
for semana in semanas:
    celulas = []
    for d in semana:
        if d.month != mes_num:
            celulas.append('<td class="cal-fora"></td>')
            continue

        categoria, descricao = status_do_dia(d)
        classes = [f'cal-{categoria}']
        if d == hoje:
            classes.append('cal-hoje')

        # Mostra a descrição curta nos dias com motivo específico
        desc_html = ''
        if categoria in ('evento', 'recesso', 'feriado'):
            desc_html = f'<span class="desc">{descricao}</span>'

        celulas.append(
            f'<td class="{" ".join(classes)}" title="{descricao}">'
            f'<span class="num">{d.day}</span>{desc_html}</td>'
        )
    linhas.append('<tr>' + ''.join(celulas) + '</tr>')

cabecalho = '<tr>' + ''.join(f'<th>{d}</th>' for d in DIAS_SEMANA) + '</tr>'
st.markdown(
    f'<table class="cal-grid">{cabecalho}{"".join(linhas)}</table>',
    unsafe_allow_html=True,
)

# ===== Controles do admin: cadastrar/remover recessos e eventos =====
if st.session_state.get('papel') == 'admin':
    st.divider()
    st.subheader('Gerenciar Recessos e Eventos')

    aba_recesso, aba_evento = st.tabs(['Recessos escolares', 'Eventos'])

    with aba_recesso:
        with st.form('novo_recesso', clear_on_submit=True):
            data_rec = st.date_input('Data', value=hoje, format='DD/MM/YYYY')
            desc_rec = st.text_input('Descrição', max_chars=80)
            if st.form_submit_button('Adicionar recesso'):
                if desc_rec.strip():
                    adicionar_recesso(data_rec.isoformat(), desc_rec.strip())
                    st.rerun()
                else:
                    st.error('Descreva o recesso antes de salvar.')

        recessos = listar_recessos()
        if not recessos:
            st.info('Nenhum recesso cadastrado.')
        else:
            for i, r in enumerate(recessos):
                c1, c2 = st.columns([5, 1])
                data_fmt = date.fromisoformat(r['data']).strftime('%d/%m/%Y')
                c1.markdown(f"**{data_fmt}** — {r['descricao']}")
                if c2.button('Remover', key=f'rec_rm_{i}'):
                    remover_recesso(i)
                    st.rerun()

    with aba_evento:
        with st.form('novo_evento', clear_on_submit=True):
            data_ev = st.date_input('Data', value=hoje, format='DD/MM/YYYY')
            desc_ev = st.text_input('Descrição', max_chars=80)
            if st.form_submit_button('Adicionar evento'):
                if desc_ev.strip():
                    adicionar_evento(data_ev.isoformat(), desc_ev.strip())
                    st.rerun()
                else:
                    st.error('Descreva o evento antes de salvar.')

        eventos = listar_eventos()
        if not eventos:
            st.info('Nenhum evento cadastrado.')
        else:
            for i, e in enumerate(eventos):
                c1, c2 = st.columns([5, 1])
                data_fmt = date.fromisoformat(e['data']).strftime('%d/%m/%Y')
                c1.markdown(f"**{data_fmt}** — {e['descricao']}")
                if c2.button('Remover', key=f'ev_rm_{i}'):
                    remover_evento(i)
                    st.rerun()
