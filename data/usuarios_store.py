# Camada de dados dos usuários (persiste em data/usuarios.json)
# Senhas armazenadas apenas como hash bcrypt; texto puro nunca é gravado.
import json
import os
import secrets
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

import bcrypt

# Papéis válidos no sistema
PAPEIS_VALIDOS = ("admin", "professor", "aluno")

# Matrículas fixas reservadas ao admin (não geradas aleatoriamente)
MATRICULAS_ADMIN = ("0001", "0002", "0003")

# Custo do bcrypt (12 = padrão recomendado em 2026)
BCRYPT_COST = 12

# Arquivo onde os usuários ficam salvos
_ARQUIVO = Path(__file__).parent / "usuarios.json"


# Lê todos os usuários do arquivo; retorna lista vazia se ainda não existir
def _carregar() -> list[dict]:
    if not _ARQUIVO.exists():
        return []
    with _ARQUIVO.open("r", encoding="utf-8") as f:
        return json.load(f)


# Grava a lista completa de usuários de forma atômica (evita corrupção em crash)
def _salvar(usuarios: list[dict]) -> None:
    _ARQUIVO.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        prefix="usuarios_", suffix=".json", dir=str(_ARQUIVO.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, _ARQUIVO)
    except Exception:
        Path(tmp_path).unlink(missing_ok=True)
        raise


# Gera o hash bcrypt de uma senha (entrada em str, hash retornado em str utf-8)
def hash_senha(senha: str) -> str:
    salt = bcrypt.gensalt(rounds=BCRYPT_COST)
    return bcrypt.hashpw(senha.encode("utf-8"), salt).decode("utf-8")


# Verifica se a senha em texto puro confere com o hash armazenado
def verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


# Sorteia uma matrícula de professor (6 dígitos) que ainda não exista
def gerar_matricula_professor() -> str:
    usuarios = _carregar()
    existentes = {u["matricula"] for u in usuarios}
    for _ in range(10_000):
        candidata = f"{secrets.randbelow(1_000_000):06d}"
        # evita colidir com matrículas reservadas do admin
        if candidata in MATRICULAS_ADMIN or candidata in existentes:
            continue
        return candidata
    raise RuntimeError("Não foi possível gerar matrícula de professor única.")


# Sorteia uma matrícula de aluno: AAAA (ano) + 8 dígitos aleatórios
def gerar_matricula_aluno(ano_matricula: int) -> str:
    if ano_matricula < 1900 or ano_matricula > 9999:
        raise ValueError("Ano de matrícula inválido.")
    usuarios = _carregar()
    existentes = {u["matricula"] for u in usuarios}
    prefixo = f"{ano_matricula:04d}"
    for _ in range(10_000):
        sufixo = f"{secrets.randbelow(100_000_000):08d}"
        candidata = prefixo + sufixo
        if candidata in existentes:
            continue
        return candidata
    raise RuntimeError("Não foi possível gerar matrícula de aluno única.")


# Gera a senha inicial padrão de um aluno: AAAA (ano) + 2 últimos dígitos da matrícula
def gerar_senha_inicial_aluno(ano_matricula: int, matricula: str) -> str:
    if ano_matricula < 1900 or ano_matricula > 9999:
        raise ValueError("Ano de matrícula inválido.")
    if not matricula or len(matricula) < 2 or not matricula.isdigit():
        raise ValueError("Matrícula inválida para derivar senha inicial.")
    return f"{ano_matricula:04d}{matricula[-2:]}"


# Cria um novo usuário e o persiste. Retorna o dict salvo (sem o hash).
def criar_usuario(
    papel: str,
    nome: str,
    senha: str,
    *,
    matricula: Optional[str] = None,
    ano_matricula: Optional[int] = None,
    deve_trocar_senha: bool = True,
) -> dict:
    if papel not in PAPEIS_VALIDOS:
        raise ValueError(f"Papel inválido: {papel}")
    if not nome or not nome.strip():
        raise ValueError("Nome é obrigatório.")
    if not senha:
        raise ValueError("Senha é obrigatória.")

    if papel == "admin":
        if matricula not in MATRICULAS_ADMIN:
            raise ValueError(
                f"Admin deve ter matrícula em {MATRICULAS_ADMIN}."
            )
    elif papel == "professor":
        matricula = matricula or gerar_matricula_professor()
    elif papel == "aluno":
        if ano_matricula is None:
            raise ValueError("ano_matricula é obrigatório para aluno.")
        matricula = matricula or gerar_matricula_aluno(ano_matricula)

    usuarios = _carregar()
    if any(u["matricula"] == matricula for u in usuarios):
        raise ValueError(f"Matrícula {matricula} já existe.")

    novo = {
        "matricula": matricula,
        "papel": papel,
        "nome": nome.strip(),
        "senha_hash": hash_senha(senha),
        "deve_trocar_senha": deve_trocar_senha,
        "ano_matricula": ano_matricula if papel == "aluno" else None,
        "criado_em": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "ultimo_login": None,
    }
    usuarios.append(novo)
    _salvar(usuarios)
    return _publico(novo)


# Retorna o usuário completo (com hash) — uso interno em auth.py
def buscar_por_matricula(matricula: str) -> Optional[dict]:
    for u in _carregar():
        if u["matricula"] == matricula:
            return u
    return None


# Atualiza a senha de um usuário e zera a flag de troca obrigatória
def atualizar_senha(matricula: str, nova_senha: str) -> None:
    if not nova_senha:
        raise ValueError("Senha é obrigatória.")
    usuarios = _carregar()
    for u in usuarios:
        if u["matricula"] == matricula:
            u["senha_hash"] = hash_senha(nova_senha)
            u["deve_trocar_senha"] = False
            _salvar(usuarios)
            return
    raise ValueError(f"Usuário {matricula} não encontrado.")


# Registra a data do último login bem-sucedido
def registrar_login(matricula: str) -> None:
    usuarios = _carregar()
    for u in usuarios:
        if u["matricula"] == matricula:
            u["ultimo_login"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
            _salvar(usuarios)
            return


# Lista usuários por papel (sem expor hash)
def listar_por_papel(papel: str) -> list[dict]:
    return [_publico(u) for u in _carregar() if u["papel"] == papel]


# Cria os 3 admins iniciais se ainda não existirem. Idempotente.
# Lê a senha inicial de ADMIN_SENHA_INICIAL (variável de ambiente).
def seed_admins() -> list[str]:
    senha_inicial = os.environ.get("ADMIN_SENHA_INICIAL")
    if not senha_inicial:
        raise RuntimeError(
            "ADMIN_SENHA_INICIAL não definida no ambiente. "
            "Configure no .env antes de iniciar."
        )
    usuarios = _carregar()
    existentes = {u["matricula"] for u in usuarios}
    criados = []
    for i, mat in enumerate(MATRICULAS_ADMIN, start=1):
        if mat in existentes:
            continue
        usuarios.append(
            {
                "matricula": mat,
                "papel": "admin",
                "nome": f"Administrador {i}",
                "senha_hash": hash_senha(senha_inicial),
                "deve_trocar_senha": True,
                "ano_matricula": None,
                "criado_em": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                "ultimo_login": None,
            }
        )
        criados.append(mat)
    if criados:
        _salvar(usuarios)
    return criados


# Versão sem campos sensíveis para exposição na UI
def _publico(u: dict) -> dict:
    return {k: v for k, v in u.items() if k != "senha_hash"}
