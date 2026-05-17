# Testes da parte pura do auth.py (validações que não dependem de Streamlit).
from auth import _formato_matricula_valido, validar_forca_senha


# ---- _formato_matricula_valido ----------------------------------------------
def test_formato_admin_4_digitos():
    assert _formato_matricula_valido("0001")
    assert _formato_matricula_valido("9999")


def test_formato_professor_6_digitos():
    assert _formato_matricula_valido("123456")


def test_formato_aluno_12_digitos():
    assert _formato_matricula_valido("202600000001")


def test_formato_invalido_tamanhos_estranhos():
    assert not _formato_matricula_valido("")
    assert not _formato_matricula_valido("12345")  # 5 dígitos
    assert not _formato_matricula_valido("1234567")  # 7 dígitos
    assert not _formato_matricula_valido("a0001")  # letra
    assert not _formato_matricula_valido("0001 ")  # espaço


# ---- validar_forca_senha ----------------------------------------------------
def test_senha_forte_aprovada():
    ok, msg = validar_forca_senha("senha-forte-1")
    assert ok and msg == ""


def test_senha_curta_rejeitada():
    ok, msg = validar_forca_senha("ab12")
    assert not ok and "mínimo" in msg


def test_senha_sem_letra_rejeitada():
    ok, msg = validar_forca_senha("12345678")
    assert not ok and "letra" in msg


def test_senha_sem_numero_rejeitada():
    ok, msg = validar_forca_senha("abcdefgh")
    assert not ok and "número" in msg


def test_senha_igual_a_atual_rejeitada():
    ok, msg = validar_forca_senha("senha-123", senha_atual="senha-123")
    assert not ok and "diferente" in msg


def test_senha_diferente_da_atual_aprovada():
    ok, msg = validar_forca_senha("senha-456", senha_atual="senha-123")
    assert ok and msg == ""
