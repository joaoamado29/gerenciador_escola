# Testes da camada de dados da grade horária
import pytest

from data import grade_store


@pytest.fixture(autouse=True)
def arquivo_temporario(tmp_path, monkeypatch):
    # Isola cada teste em um grade.json próprio (recriado a cada teste)
    monkeypatch.setattr(grade_store, '_ARQUIVO', tmp_path / 'grade.json')


def test_constantes_basicas():
    assert len(grade_store.TURMAS) == 10
    assert grade_store.DIAS == ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    assert grade_store.TURNOS == ['Manhã', 'Tarde']
    assert len(grade_store.DISCIPLINAS) == 12


def test_horarios_de_aula_tem_seis_slots_por_turno():
    for turno in grade_store.TURNOS:
        assert len(grade_store.HORARIOS_AULAS[turno]) == 6


def test_horarios_manha_respeitam_intervalo_e_saida():
    slots = grade_store.HORARIOS_AULAS['Manhã']
    assert slots[0] == ('07:00', '07:50')
    assert slots[2][1] == '09:30'  # 3ª aula termina antes do intervalo
    assert slots[3][0] == '09:50'  # 4ª aula começa depois do intervalo
    assert slots[5][1] == '12:20'  # saída
    assert grade_store.INTERVALO['Manhã'] == ('09:30', '09:50')


def test_horarios_tarde_respeitam_intervalo_e_saida():
    slots = grade_store.HORARIOS_AULAS['Tarde']
    assert slots[0] == ('13:00', '13:50')
    assert slots[2][1] == '15:30'
    assert slots[3][0] == '15:50'
    assert slots[5][1] == '18:20'
    assert grade_store.INTERVALO['Tarde'] == ('15:30', '15:50')


def test_seed_inicial_tem_grade_completa_para_cada_turma():
    # Acessar qualquer função força a criação do arquivo com seed
    for turma in grade_store.TURMAS:
        grade = grade_store.grade_da_turma(turma)
        assert set(grade.keys()) == set(grade_store.DIAS)
        for dia in grade_store.DIAS:
            assert len(grade[dia]) == 6
            for materia in grade[dia]:
                assert materia in grade_store.DISCIPLINAS


def test_turno_padrao_de_cada_turma():
    assert grade_store.turno_da_turma('1º A') == 'Manhã'
    assert grade_store.turno_da_turma('2º A') == 'Tarde'
    assert grade_store.turno_da_turma('3º C') == 'Manhã'


def test_atualizar_aula_persiste():
    grade_store.atualizar_aula('1º A', 'Segunda', 0, 'Inglês')
    assert grade_store.grade_da_turma('1º A')['Segunda'][0] == 'Inglês'


def test_atualizar_turno_persiste():
    grade_store.atualizar_turno('1º A', 'Tarde')
    assert grade_store.turno_da_turma('1º A') == 'Tarde'


def test_aulas_do_dia_inclui_horarios_e_disciplinas():
    grade_store.atualizar_aula('1º A', 'Quarta', 0, 'Matemática')
    aulas = grade_store.aulas_do_dia('1º A', 'Quarta')
    assert len(aulas) == 6
    assert aulas[0]['hora_inicio'] == '07:00'
    assert aulas[0]['hora_fim'] == '07:50'
    assert aulas[0]['disciplina'] == 'Matemática'


def test_aulas_do_professor_filtra_por_disciplina_dia_turno():
    # Limpa Segunda em todas as turmas e planta 'Matemática' só onde queremos
    for turma in grade_store.TURMAS:
        for i in range(6):
            grade_store.atualizar_aula(turma, 'Segunda', i, 'Português')
    grade_store.atualizar_aula('1º A', 'Segunda', 0, 'Matemática')  # Manhã
    grade_store.atualizar_aula('2º B', 'Segunda', 2, 'Matemática')  # Tarde

    aulas_manha = grade_store.aulas_do_professor('Matemática', 'Segunda', 'Manhã')
    assert len(aulas_manha) == 1
    assert aulas_manha[0]['turma'] == '1º A'
    assert aulas_manha[0]['indice_aula'] == 1
    assert aulas_manha[0]['hora_inicio'] == '07:00'

    aulas_tarde = grade_store.aulas_do_professor('Matemática', 'Segunda', 'Tarde')
    assert len(aulas_tarde) == 1
    assert aulas_tarde[0]['turma'] == '2º B'
    assert aulas_tarde[0]['indice_aula'] == 3


def test_aulas_do_professor_vazio_quando_nao_ha_match():
    for turma in grade_store.TURMAS:
        for i in range(6):
            grade_store.atualizar_aula(turma, 'Sexta', i, 'Português')
    assert grade_store.aulas_do_professor('Filosofia', 'Sexta', 'Manhã') == []
