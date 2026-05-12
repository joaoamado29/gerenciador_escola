# Testes da camada de dados de turmas
from streamlit.testing.v1 import AppTest

from data.turmas import (
    ANOS,
    CLASSES,
    TURNOS,
    ALUNOS_POR_TURMA,
    alunos_da_turma,
)

TIMEOUT = 30


def test_constantes_basicas():
    assert ANOS == ['1º ano', '2º ano', '3º ano']
    assert CLASSES == ['Classe A', 'Classe B', 'Classe C']
    assert TURNOS == ['Manhã', 'Tarde', 'Noite']


def test_alunos_por_turma_cobre_todas_as_combinacoes():
    # 3 anos * 3 classes * 3 turnos = 27 turmas
    assert len(ALUNOS_POR_TURMA) == 27
    for ano in ANOS:
        for classe in CLASSES:
            for turno in TURNOS:
                assert (ano, classe, turno) in ALUNOS_POR_TURMA


def test_cada_turma_tem_dois_alunos_de_strings_nao_vazias():
    for turma, alunos in ALUNOS_POR_TURMA.items():
        assert len(alunos) == 2, f'Turma {turma} deve ter 2 alunos'
        for nome in alunos:
            assert isinstance(nome, str)
            assert nome.strip(), f'Nome vazio em {turma}'


def test_alunos_da_turma_existente():
    turma = ('1º ano', 'Classe A', 'Manhã')
    assert alunos_da_turma(turma) == ['Ana Silva', 'Bruno Souza']


def test_alunos_da_turma_inexistente_retorna_lista_vazia():
    assert alunos_da_turma(('inexistente', 'X', 'Y')) == []


def test_selecionar_turma_renderiza_tres_selectboxes():
    # Usa AppTest para executar a função dentro de um app Streamlit fake
    def script():
        from data.turmas import selecionar_turma
        selecionar_turma()

    at = AppTest.from_function(script, default_timeout=TIMEOUT)
    at.run()
    assert not at.exception
    assert len(at.selectbox) == 3
    assert at.selectbox[0].label == 'Ano:'
    assert at.selectbox[1].label == 'Classe:'
    assert at.selectbox[2].label == 'Turno:'
