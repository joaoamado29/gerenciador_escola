# Testes da camada de dados dos avisos da coordenação
import pytest

from data import avisos_store


@pytest.fixture(autouse=True)
def arquivo_temporario(tmp_path, monkeypatch):
    # Isola cada teste em um avisos.json próprio dentro de tmp_path
    monkeypatch.setattr(avisos_store, '_ARQUIVO', tmp_path / 'avisos.json')


def test_publicos_disponiveis():
    assert avisos_store.PUBLICOS == ['Todos', 'Professores', 'Alunos']


def test_listar_sem_arquivo_retorna_lista_vazia():
    assert avisos_store.listar_avisos() == []


def test_adicionar_cria_arquivo_e_grava_aviso():
    avisos_store.adicionar_aviso('Título', 'Mensagem', 'Todos')
    avisos = avisos_store.listar_avisos()
    assert len(avisos) == 1
    assert avisos[0]['id'] == 1
    assert avisos[0]['titulo'] == 'Título'
    assert avisos[0]['mensagem'] == 'Mensagem'
    assert avisos[0]['publico'] == 'Todos'
    assert avisos[0]['data']


def test_adicionar_insere_no_topo_com_id_incremental():
    avisos_store.adicionar_aviso('Primeiro', 'msg', 'Todos')
    avisos_store.adicionar_aviso('Segundo', 'msg', 'Alunos')
    avisos = avisos_store.listar_avisos()
    assert [a['titulo'] for a in avisos] == ['Segundo', 'Primeiro']
    assert [a['id'] for a in avisos] == [2, 1]


def test_remover_aviso_por_id():
    avisos_store.adicionar_aviso('Primeiro', 'msg', 'Todos')
    avisos_store.adicionar_aviso('Segundo', 'msg', 'Todos')
    avisos_store.remover_aviso(1)
    avisos = avisos_store.listar_avisos()
    assert len(avisos) == 1
    assert avisos[0]['titulo'] == 'Segundo'


def test_remover_id_inexistente_nao_altera_nada():
    avisos_store.adicionar_aviso('Único', 'msg', 'Todos')
    avisos_store.remover_aviso(999)
    assert len(avisos_store.listar_avisos()) == 1


def test_avisos_para_professor_inclui_todos_e_professores():
    avisos_store.adicionar_aviso('Geral', 'msg', 'Todos')
    avisos_store.adicionar_aviso('Só professores', 'msg', 'Professores')
    avisos_store.adicionar_aviso('Só alunos', 'msg', 'Alunos')
    titulos = [a['titulo'] for a in avisos_store.avisos_para('professor')]
    assert titulos == ['Só professores', 'Geral']


def test_avisos_para_aluno_inclui_todos_e_alunos():
    avisos_store.adicionar_aviso('Geral', 'msg', 'Todos')
    avisos_store.adicionar_aviso('Só professores', 'msg', 'Professores')
    avisos_store.adicionar_aviso('Só alunos', 'msg', 'Alunos')
    titulos = [a['titulo'] for a in avisos_store.avisos_para('aluno')]
    assert titulos == ['Só alunos', 'Geral']


def test_avisos_para_admin_ve_todos():
    avisos_store.adicionar_aviso('Geral', 'msg', 'Todos')
    avisos_store.adicionar_aviso('Só professores', 'msg', 'Professores')
    avisos_store.adicionar_aviso('Só alunos', 'msg', 'Alunos')
    titulos = [a['titulo'] for a in avisos_store.avisos_para('admin')]
    assert titulos == ['Só alunos', 'Só professores', 'Geral']
