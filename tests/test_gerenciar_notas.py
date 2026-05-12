# Testes da página de gerenciar notas (professor)
from streamlit.testing.v1 import AppTest

SCRIPT = 'pages/professor/gerenciar_notas.py'
TIMEOUT = 30


def _at():
    return AppTest.from_file(SCRIPT, default_timeout=TIMEOUT)


def test_pagina_carrega_sem_erro():
    at = _at()
    at.run()
    assert not at.exception
    assert at.title[0].value == 'Gerenciar Notas'


def test_renderiza_selectboxes_turma_aluno_bimestre():
    at = _at()
    at.run()
    labels = [s.label for s in at.selectbox]
    # Ano, Classe, Turno, Aluno, Bimestre
    assert labels == ['Ano:', 'Classe:', 'Turno:', 'Aluno:', 'Bimestre:']


def test_inputs_de_nota_com_bounds_0_a_10():
    at = _at()
    at.run()
    assert len(at.number_input) == 2
    for inp in at.number_input:
        assert inp.min == 0.0
        assert inp.max == 10.0
        assert inp.step == 0.1


def test_envia_notas_validas_e_calcula_media():
    at = _at()
    at.run()
    at.number_input[0].set_value(8.0)
    at.number_input[1].set_value(6.0)
    at.button[0].click().run()
    assert not at.exception
    sucessos = ' '.join(s.value or '' for s in at.success)
    # Média de 8.0 e 6.0 = 7.00
    assert '7.00' in sucessos


def test_envia_sem_preencher_mostra_erro():
    at = _at()
    at.run()
    at.button[0].click().run()
    assert not at.exception
    erros = ' '.join(e.value or '' for e in at.error)
    assert 'Preencha as duas notas' in erros


def test_envia_so_uma_nota_mostra_erro():
    at = _at()
    at.run()
    at.number_input[0].set_value(7.5)
    at.button[0].click().run()
    erros = ' '.join(e.value or '' for e in at.error)
    assert 'Preencha as duas notas' in erros
