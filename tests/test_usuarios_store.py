# Testes do data/usuarios_store.py — usa tmp_path para isolar o arquivo JSON.
import importlib

import pytest


@pytest.fixture
def store(tmp_path, monkeypatch):
    # Recarrega o módulo apontando _ARQUIVO para um arquivo temporário
    import data.usuarios_store as mod
    importlib.reload(mod)
    monkeypatch.setattr(mod, "_ARQUIVO", tmp_path / "usuarios.json")
    return mod


def test_hash_e_verificacao(store):
    h = store.hash_senha("senha-forte-123")
    assert h != "senha-forte-123"
    assert store.verificar_senha("senha-forte-123", h) is True
    assert store.verificar_senha("errada", h) is False


def test_verificar_senha_hash_invalido_nao_lanca(store):
    assert store.verificar_senha("qualquer", "hash-bagunçado") is False


def test_criar_professor_gera_matricula_de_6_digitos(store):
    criado = store.criar_usuario(
        papel="professor", nome="Maria", senha="senha123"
    )
    assert criado["papel"] == "professor"
    assert len(criado["matricula"]) == 6
    assert criado["matricula"].isdigit()
    assert "senha_hash" not in criado  # _publico não expõe hash


def test_criar_aluno_prefixa_ano_e_tem_12_digitos(store):
    criado = store.criar_usuario(
        papel="aluno", nome="João", senha="2026",
        ano_matricula=2026,
    )
    assert criado["matricula"].startswith("2026")
    assert len(criado["matricula"]) == 12
    assert criado["ano_matricula"] == 2026


def test_gerar_senha_inicial_aluno_formato(store):
    s = store.gerar_senha_inicial_aluno(2026, "202647829103")
    assert s == "202603"  # ano + dois últimos dígitos da matrícula
    assert len(s) == 6
    assert s.isdigit()


def test_gerar_senha_inicial_aluno_ano_invalido(store):
    import pytest as _pt
    with _pt.raises(ValueError):
        store.gerar_senha_inicial_aluno(123, "202600000099")


def test_gerar_senha_inicial_aluno_matricula_invalida(store):
    import pytest as _pt
    with _pt.raises(ValueError):
        store.gerar_senha_inicial_aluno(2026, "")
    with _pt.raises(ValueError):
        store.gerar_senha_inicial_aluno(2026, "x")
    with _pt.raises(ValueError):
        store.gerar_senha_inicial_aluno(2026, "20a6")


def test_criar_admin_exige_matricula_reservada(store):
    with pytest.raises(ValueError):
        store.criar_usuario(papel="admin", nome="X", senha="senha123")
    with pytest.raises(ValueError):
        store.criar_usuario(
            papel="admin", nome="X", senha="senha123", matricula="9999"
        )
    ok = store.criar_usuario(
        papel="admin", nome="Admin 1", senha="senha123", matricula="0001"
    )
    assert ok["matricula"] == "0001"


def test_criar_aluno_sem_ano_falha(store):
    with pytest.raises(ValueError):
        store.criar_usuario(papel="aluno", nome="X", senha="2026")


def test_papel_invalido_falha(store):
    with pytest.raises(ValueError):
        store.criar_usuario(papel="diretor", nome="X", senha="senha123")


def test_matricula_duplicada_falha(store):
    store.criar_usuario(
        papel="admin", nome="A1", senha="senha123", matricula="0001"
    )
    with pytest.raises(ValueError):
        store.criar_usuario(
            papel="admin", nome="A1 dup", senha="senha123", matricula="0001"
        )


def test_atualizar_senha_zera_flag_de_troca(store):
    store.criar_usuario(
        papel="admin", nome="A", senha="antiga12",
        matricula="0001", deve_trocar_senha=True,
    )
    store.atualizar_senha("0001", "nova-senha-456")
    u = store.buscar_por_matricula("0001")
    assert u["deve_trocar_senha"] is False
    assert store.verificar_senha("nova-senha-456", u["senha_hash"])
    assert not store.verificar_senha("antiga12", u["senha_hash"])


def test_atualizar_senha_usuario_inexistente_falha(store):
    with pytest.raises(ValueError):
        store.atualizar_senha("9999", "qualquer-12")


def test_listar_por_papel_nao_expoe_hash(store):
    store.criar_usuario(
        papel="admin", nome="A", senha="senha123", matricula="0001"
    )
    store.criar_usuario(papel="professor", nome="P", senha="senha123")
    admins = store.listar_por_papel("admin")
    profs = store.listar_por_papel("professor")
    assert len(admins) == 1 and len(profs) == 1
    assert all("senha_hash" not in u for u in admins + profs)


def test_seed_admins_idempotente(store, monkeypatch):
    monkeypatch.setenv("ADMIN_SENHA_INICIAL", "admin-inicial-99")
    criados1 = store.seed_admins()
    assert set(criados1) == {"0001", "0002", "0003"}
    # segunda chamada não cria nada
    criados2 = store.seed_admins()
    assert criados2 == []
    # todos com deve_trocar_senha=True
    for mat in ("0001", "0002", "0003"):
        u = store.buscar_por_matricula(mat)
        assert u["deve_trocar_senha"] is True
        assert store.verificar_senha("admin-inicial-99", u["senha_hash"])


def test_seed_admins_sem_env_falha(store, monkeypatch):
    monkeypatch.delenv("ADMIN_SENHA_INICIAL", raising=False)
    with pytest.raises(RuntimeError):
        store.seed_admins()


def test_gerar_matricula_aluno_ano_invalido(store):
    with pytest.raises(ValueError):
        store.gerar_matricula_aluno(123)
    with pytest.raises(ValueError):
        store.gerar_matricula_aluno(10_000)
