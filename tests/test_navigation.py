# Testes da estrutura de navegação
from pathlib import Path

from streamlit.testing.v1 import AppTest

TIMEOUT = 30
ROOT = Path(__file__).resolve().parents[1]


def test_app_principal_exibe_tela_de_login():
    # Sem usuário autenticado, app.py deve renderizar a tela de login
    # (não a navegação interna). Garante que o gate de autenticação está ativo.
    import os
    os.environ.setdefault('ADMIN_SENHA_INICIAL', 'teste-inicial-1')
    at = AppTest.from_file('app.py', default_timeout=TIMEOUT)
    at.run()
    assert not at.exception
    assert any('Acesso ao sistema' in (t.value or '') for t in at.title)


def test_app_apos_login_carrega_navegacao_do_papel(tmp_path, monkeypatch):
    # Simula sessão autenticada via session_state e confirma que a navegação
    # do papel correspondente é renderizada (página inicial = escola).
    import os
    os.environ.setdefault('ADMIN_SENHA_INICIAL', 'teste-inicial-1')
    at = AppTest.from_file('app.py', default_timeout=TIMEOUT)
    at.session_state['autenticado'] = True
    at.session_state['matricula'] = '000000'
    at.session_state['papel'] = 'professor'
    at.session_state['nome'] = 'Teste'
    at.session_state['deve_trocar_senha'] = False
    at.run()
    assert not at.exception
    assert any('Escola Estadual Machado de Assis' in (t.value or '') for t in at.title)


def _run_nav_via_temp_script(nav_func_name, tmp_path):
    # Cria um app temporário dentro da raiz do projeto para que os caminhos
    # relativos de st.Page (ex.: pages/shared/inicio.py) sejam encontrados.
    script_path = ROOT / '_tmp_nav_test.py'
    script_path.write_text(
        f'from pages.navigation import {nav_func_name}\n{nav_func_name}()\n',
        encoding='utf-8',
    )
    try:
        at = AppTest.from_file(str(script_path), default_timeout=TIMEOUT)
        at.run()
        return at
    finally:
        script_path.unlink(missing_ok=True)


def test_nav_aluno_executa_sem_erro(tmp_path):
    at = _run_nav_via_temp_script('nav_aluno', tmp_path)
    assert not at.exception


def test_nav_admin_executa_sem_erro(tmp_path):
    at = _run_nav_via_temp_script('nav_admin', tmp_path)
    assert not at.exception
