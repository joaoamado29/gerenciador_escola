# Testes do helper de carregamento de CSS
from streamlit.testing.v1 import AppTest

TIMEOUT = 30


def test_load_css_le_arquivo_e_injeta_markdown(tmp_path):
    css_file = tmp_path / 'estilo.css'
    css_file.write_text('body { color: red; }', encoding='utf-8')

    # from_string permite usar variáveis externas via f-string
    script = f"""
from ui.styles import load_css
load_css(r'{css_file}')
"""
    at = AppTest.from_string(script, default_timeout=TIMEOUT)
    at.run()
    assert not at.exception
    # load_css usa st.markdown com unsafe_allow_html para injetar <style>
    assert any('body { color: red; }' in (m.value or '') for m in at.markdown)


def test_load_css_levanta_erro_se_arquivo_nao_existe():
    script = """
from ui.styles import load_css
load_css('caminho/que/nao/existe.css')
"""
    at = AppTest.from_string(script, default_timeout=TIMEOUT)
    at.run()
    # FileNotFoundError deve borbulhar como exceção do app
    assert at.exception
