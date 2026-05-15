# Camada de dados dos avisos da coordenação (persiste em data/avisos.json)
import json
from datetime import datetime
from pathlib import Path

# Públicos que um aviso pode ter como destino
PUBLICOS = ['Todos', 'Professores', 'Alunos']

# Arquivo onde os avisos ficam salvos
_ARQUIVO = Path(__file__).parent / 'avisos.json'


# Lê todos os avisos do arquivo; retorna lista vazia se ainda não existir
def listar_avisos():
    if not _ARQUIVO.exists():
        return []
    with _ARQUIVO.open(encoding='utf-8') as f:
        return json.load(f)


# Grava a lista completa de avisos no arquivo
def _salvar(avisos):
    with _ARQUIVO.open('w', encoding='utf-8') as f:
        json.dump(avisos, f, ensure_ascii=False, indent=2)


# Cria um novo aviso e o salva no topo da lista
def adicionar_aviso(titulo, mensagem, publico):
    avisos = listar_avisos()
    novo_id = max((a['id'] for a in avisos), default=0) + 1
    avisos.insert(0, {
        'id': novo_id,
        'titulo': titulo,
        'mensagem': mensagem,
        'publico': publico,
        'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
    })
    _salvar(avisos)


# Remove um aviso pelo id
def remover_aviso(aviso_id):
    avisos = [a for a in listar_avisos() if a['id'] != aviso_id]
    _salvar(avisos)


# Devolve só os avisos visíveis para um tipo de usuário ('professor' / 'aluno')
def avisos_para(papel):
    alvo = 'Professores' if papel == 'professor' else 'Alunos'
    return [a for a in listar_avisos() if a['publico'] in ('Todos', alvo)]
