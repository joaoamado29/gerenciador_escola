# Testes da página de gerenciar frequência (professor)
from streamlit.testing.v1 import AppTest

SCRIPT = 'pages/professor/gerenciar_frequencia.py'
TIMEOUT = 30


def _at():
    return AppTest.from_file(SCRIPT, default_timeout=TIMEOUT)


def test_pagina_carrega_sem_erro():
    at = _at()
    at.run()
    assert not at.exception
    assert at.title[0].value == 'Gerenciar Frequência'


def test_renderiza_selectboxes_de_turma():
    at = _at()
    at.run()
    labels = [s.label for s in at.selectbox]
    assert 'Ano:' in labels
    assert 'Classe:' in labels
    assert 'Turno:' in labels


def test_lista_alunos_da_turma_default():
    # Default: 1º ano, Classe A, Manhã -> Ana Silva, Bruno Souza
    at = _at()
    at.run()
    nomes_renderizados = ' '.join(m.value or '' for m in at.markdown)
    assert 'Ana Silva' in nomes_renderizados
    assert 'Bruno Souza' in nomes_renderizados


def test_radios_de_frequencia_um_por_aluno():
    at = _at()
    at.run()
    # Turma default tem 2 alunos -> 2 radios
    assert len(at.radio) == 2
    for r in at.radio:
        assert list(r.options) == ['Presente', 'Falta', 'Falta Justificada']


def test_botao_salvar_exibe_resumo():
    at = _at()
    at.run()
    at.radio[0].set_value('Falta').run()
    at.button[0].click().run()
    assert not at.exception
    sucessos = ' '.join(s.value or '' for s in at.success)
    assert 'Frequência registrada' in sucessos


def test_troca_de_turma_atualiza_lista_de_alunos():
    at = _at()
    at.run()
    # Muda Classe para B (1º ano, Classe B, Manhã -> Gabriela Dias, Henrique Melo)
    at.selectbox[1].set_value('Classe B').run()
    nomes = ' '.join(m.value or '' for m in at.markdown)
    assert 'Gabriela Dias' in nomes
    assert 'Henrique Melo' in nomes
    assert 'Ana Silva' not in nomes
