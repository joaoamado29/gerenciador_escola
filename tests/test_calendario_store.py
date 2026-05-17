# Testes da camada de dados do calendário letivo
from datetime import date

import pytest

from data import calendario_store


@pytest.fixture(autouse=True)
def arquivo_temporario(tmp_path, monkeypatch):
    # Isola cada teste em um calendario.json próprio
    monkeypatch.setattr(
        calendario_store, '_ARQUIVO', tmp_path / 'calendario.json'
    )


def test_constantes_basicas():
    assert len(calendario_store.MESES) == 12
    assert calendario_store.MESES[0] == 'Janeiro'
    assert calendario_store.MESES[11] == 'Dezembro'
    assert len(calendario_store.DIAS_SEMANA) == 7


def test_listar_sem_arquivo_retorna_vazio():
    assert calendario_store.listar_recessos() == []
    assert calendario_store.listar_eventos() == []


def test_adicionar_recesso_persiste():
    calendario_store.adicionar_recesso('2026-06-10', 'Recesso da escola')
    recessos = calendario_store.listar_recessos()
    assert len(recessos) == 1
    assert recessos[0] == {'data': '2026-06-10', 'descricao': 'Recesso da escola'}


def test_adicionar_evento_persiste():
    calendario_store.adicionar_evento('2026-08-20', 'Feira de ciências')
    eventos = calendario_store.listar_eventos()
    assert len(eventos) == 1
    assert eventos[0] == {'data': '2026-08-20', 'descricao': 'Feira de ciências'}


def test_remover_recesso_por_indice():
    calendario_store.adicionar_recesso('2026-06-10', 'Primeiro')
    calendario_store.adicionar_recesso('2026-06-11', 'Segundo')
    calendario_store.remover_recesso(0)
    assert [r['descricao'] for r in calendario_store.listar_recessos()] == ['Segundo']


def test_remover_evento_por_indice():
    calendario_store.adicionar_evento('2026-08-20', 'Primeiro')
    calendario_store.adicionar_evento('2026-08-21', 'Segundo')
    calendario_store.remover_evento(1)
    assert [e['descricao'] for e in calendario_store.listar_eventos()] == ['Primeiro']


def test_segunda_segunda_dezembro_2026():
    # Dez/2026: 1ª segunda = 07/12 → 2ª segunda = 14/12
    assert calendario_store.segunda_segunda_dezembro(2026) == date(2026, 12, 14)


def test_segunda_segunda_dezembro_2024():
    # Dez/2024: 1ª segunda = 02/12 → 2ª segunda = 09/12
    assert calendario_store.segunda_segunda_dezembro(2024) == date(2024, 12, 9)


def test_feriados_nacionais_inclui_principais():
    feriados = calendario_store.feriados_nacionais(2026)
    assert date(2026, 1, 1) in feriados
    assert date(2026, 5, 1) in feriados
    assert date(2026, 9, 7) in feriados
    assert date(2026, 12, 25) in feriados


def test_status_ferias_em_janeiro_e_julho():
    assert calendario_store.status_do_dia(date(2026, 1, 15))[0] == 'ferias'
    assert calendario_store.status_do_dia(date(2026, 7, 4))[0] == 'ferias'


def test_status_feriado_dia_de_semana():
    # 01/05/2026 = sexta-feira (Dia do Trabalho)
    categoria, descricao = calendario_store.status_do_dia(date(2026, 5, 1))
    assert categoria == 'feriado'
    assert descricao


def test_status_fim_de_semana():
    # 16/05/2026 = sábado
    assert calendario_store.status_do_dia(date(2026, 5, 16))[0] == 'fim_de_semana'
    # 17/05/2026 = domingo
    assert calendario_store.status_do_dia(date(2026, 5, 17))[0] == 'fim_de_semana'


def test_status_dia_letivo():
    # 18/05/2026 = segunda-feira sem feriado
    assert calendario_store.status_do_dia(date(2026, 5, 18))[0] == 'letivo'


def test_status_recuperacao_a_partir_da_segunda_segunda_de_dezembro():
    # 14/12/2026 = 2ª segunda de dezembro
    assert calendario_store.status_do_dia(date(2026, 12, 14))[0] == 'recuperacao'
    assert calendario_store.status_do_dia(date(2026, 12, 15))[0] == 'recuperacao'
    # 07/12/2026 = 1ª segunda (ainda não é recuperação)
    assert calendario_store.status_do_dia(date(2026, 12, 7))[0] == 'letivo'


def test_status_feriado_tem_precedencia_sobre_recuperacao():
    # 25/12 cai durante o período de recuperação, mas continua sendo feriado
    categoria, _ = calendario_store.status_do_dia(date(2026, 12, 25))
    assert categoria == 'feriado'


def test_status_evento_cadastrado_pelo_admin():
    calendario_store.adicionar_evento('2026-05-20', 'Feira cultural')
    categoria, descricao = calendario_store.status_do_dia(date(2026, 5, 20))
    assert categoria == 'evento'
    assert descricao == 'Feira cultural'


def test_status_recesso_cadastrado_pelo_admin():
    calendario_store.adicionar_recesso('2026-05-22', 'Ponte do feriado')
    categoria, descricao = calendario_store.status_do_dia(date(2026, 5, 22))
    assert categoria == 'recesso'
    assert descricao == 'Ponte do feriado'


def test_evento_tem_precedencia_sobre_recesso():
    calendario_store.adicionar_evento('2026-05-25', 'Reunião pedagógica')
    calendario_store.adicionar_recesso('2026-05-25', 'Recesso')
    categoria, _ = calendario_store.status_do_dia(date(2026, 5, 25))
    assert categoria == 'evento'


def test_ferias_tem_precedencia_sobre_evento():
    # Mesmo se admin marcar evento em julho, continua sendo férias
    calendario_store.adicionar_evento('2026-07-15', 'Curso de férias')
    categoria, _ = calendario_store.status_do_dia(date(2026, 7, 15))
    assert categoria == 'ferias'
