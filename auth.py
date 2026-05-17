# Camada de autenticação: login, logout, troca de senha e proteção da sessão.
# Não armazena senha em texto puro nem em st.session_state — só hash via usuarios_store.
import re
import time

import streamlit as st

from data.usuarios_store import (
    MATRICULAS_ADMIN,
    atualizar_senha,
    buscar_por_matricula,
    registrar_login,
    seed_admins,
    verificar_senha,
)

# Política de tentativas: após N falhas, bloqueia por T segundos (por sessão)
MAX_TENTATIVAS = 5
BLOQUEIO_SEGUNDOS = 60

# Política mínima de senha (aplicada apenas na troca, não no login inicial)
SENHA_MIN_LEN = 8


# Valida o formato da matrícula. Aceita 4 (admin), 6 (professor) ou 12 (aluno) dígitos.
def _formato_matricula_valido(matricula: str) -> bool:
    return bool(re.fullmatch(r"\d{4}|\d{6}|\d{12}", matricula or ""))


# Retorna (ok, mensagem). Política mínima: 8+ chars, 1 letra, 1 número.
def validar_forca_senha(senha: str, senha_atual: str = "") -> tuple[bool, str]:
    if not senha or len(senha) < SENHA_MIN_LEN:
        return False, f"A senha deve ter no mínimo {SENHA_MIN_LEN} caracteres."
    if not re.search(r"[A-Za-zÀ-ÿ]", senha):
        return False, "A senha deve conter pelo menos uma letra."
    if not re.search(r"\d", senha):
        return False, "A senha deve conter pelo menos um número."
    if senha_atual and senha == senha_atual:
        return False, "A nova senha deve ser diferente da atual."
    return True, ""


# Verifica se há bloqueio ativo por excesso de tentativas; retorna segundos restantes.
def _segundos_de_bloqueio() -> int:
    bloqueado_ate = st.session_state.get("auth_bloqueado_ate", 0)
    restante = int(bloqueado_ate - time.time())
    return max(0, restante)


# Registra uma tentativa falha; aciona o bloqueio quando atinge o limite.
def _registrar_falha() -> None:
    tentativas = st.session_state.get("auth_tentativas", 0) + 1
    st.session_state["auth_tentativas"] = tentativas
    if tentativas >= MAX_TENTATIVAS:
        st.session_state["auth_bloqueado_ate"] = time.time() + BLOQUEIO_SEGUNDOS


# Limpa contadores após login bem-sucedido
def _limpar_tentativas() -> None:
    st.session_state.pop("auth_tentativas", None)
    st.session_state.pop("auth_bloqueado_ate", None)


# True se a sessão atual tem usuário autenticado
def usuario_logado() -> bool:
    return bool(st.session_state.get("autenticado"))


# Encerra a sessão; preserva apenas chaves de UI alheias ao auth
def logout() -> None:
    for chave in (
        "autenticado",
        "matricula",
        "papel",
        "nome",
        "deve_trocar_senha",
        "auth_tentativas",
        "auth_bloqueado_ate",
    ):
        st.session_state.pop(chave, None)


# Cria a sessão a partir de um usuário já validado (sem hash em session_state)
def _iniciar_sessao(usuario: dict) -> None:
    st.session_state["autenticado"] = True
    st.session_state["matricula"] = usuario["matricula"]
    st.session_state["papel"] = usuario["papel"]
    st.session_state["nome"] = usuario["nome"]
    st.session_state["deve_trocar_senha"] = usuario.get("deve_trocar_senha", False)


# Garante que os 3 admins existem antes do primeiro login (idempotente)
def _garantir_admins() -> None:
    if st.session_state.get("auth_seed_ok"):
        return
    try:
        seed_admins()
        st.session_state["auth_seed_ok"] = True
    except RuntimeError as e:
        st.error(str(e))
        st.stop()


# Tela de login. Renderiza o formulário e processa a submissão.
def tela_login() -> None:
    _garantir_admins()

    st.title("Acesso ao sistema")
    st.caption("Entre com sua matrícula e senha.")

    bloqueio = _segundos_de_bloqueio()
    if bloqueio > 0:
        st.error(
            f"Muitas tentativas. Tente novamente em {bloqueio} segundos."
        )
        return

    with st.form("form_login", clear_on_submit=False):
        matricula = st.text_input("Matrícula", max_chars=12).strip()
        senha = st.text_input("Senha", type="password")
        enviar = st.form_submit_button("Entrar", type="primary")

    if not enviar:
        return

    # Validação de formato antes de consultar o store (não vaza qual campo falhou)
    if not _formato_matricula_valido(matricula) or not senha:
        _registrar_falha()
        st.error("Matrícula ou senha inválida.")
        return

    usuario = buscar_por_matricula(matricula)
    # Mesma mensagem para "não existe" e "senha errada" — evita user enumeration
    if usuario is None or not verificar_senha(senha, usuario["senha_hash"]):
        _registrar_falha()
        st.error("Matrícula ou senha inválida.")
        return

    _limpar_tentativas()
    registrar_login(usuario["matricula"])
    _iniciar_sessao(usuario)
    st.rerun()


# Tela de troca obrigatória de senha (primeiro login ou solicitada pelo usuário)
def tela_trocar_senha(obrigatoria: bool = False) -> None:
    st.title("Trocar senha")
    if obrigatoria:
        st.warning(
            "Este é seu primeiro acesso. Defina uma nova senha para continuar."
        )

    with st.form("form_trocar_senha", clear_on_submit=True):
        atual = st.text_input("Senha atual", type="password")
        nova = st.text_input("Nova senha", type="password")
        confirmar = st.text_input("Confirmar nova senha", type="password")
        enviar = st.form_submit_button("Salvar", type="primary")

    if not enviar:
        return

    matricula = st.session_state.get("matricula")
    usuario = buscar_por_matricula(matricula) if matricula else None
    if usuario is None or not verificar_senha(atual, usuario["senha_hash"]):
        st.error("Senha atual incorreta.")
        return

    if nova != confirmar:
        st.error("A confirmação não confere com a nova senha.")
        return

    ok, msg = validar_forca_senha(nova, senha_atual=atual)
    if not ok:
        st.error(msg)
        return

    atualizar_senha(matricula, nova)
    st.session_state["deve_trocar_senha"] = False
    st.success("Senha atualizada com sucesso.")
    st.rerun()


# Gate completo: exibe login ou troca obrigatória; só retorna True se liberado
def exigir_autenticacao() -> bool:
    if not usuario_logado():
        tela_login()
        return False
    if st.session_state.get("deve_trocar_senha"):
        tela_trocar_senha(obrigatoria=True)
        return False
    return True
