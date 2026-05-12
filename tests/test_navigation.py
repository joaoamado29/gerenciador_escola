# Testes da estrutura de navegação
from pathlib import Path

from streamlit.testing.v1 import AppTest

TIMEOUT = 30
ROOT = Path(__file__).resolve().parents[1]


def test_app_principal_carrega_navegacao_professor():
    at = AppTest.from_file('app.py', default_timeout=TIMEOUT)
    at.run()
    assert not at.exception
    # A navegação do professor inicia na página "Início"
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
