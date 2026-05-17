# Camada de dados do calendário letivo (persiste em data/calendario.json)
import json
from datetime import date, timedelta
from pathlib import Path

import holidays

# Nomes em português usados pela UI
MESES = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro',
]
DIAS_SEMANA = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

# Arquivo onde recessos e eventos (cadastrados pelo admin) ficam salvos
_ARQUIVO = Path(__file__).parent / 'calendario.json'


def _carregar():
    if not _ARQUIVO.exists():
        _salvar({'recessos': [], 'eventos': []})
    with _ARQUIVO.open(encoding='utf-8') as f:
        return json.load(f)


def _salvar(dados):
    with _ARQUIVO.open('w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


# Feriados nacionais brasileiros (lib `holidays`, com pontos facultativos).
# categories=('public','optional') inclui Carnaval e Sexta-feira Santa.
def feriados_nacionais(ano):
    return holidays.country_holidays(
        'BR', years=ano, categories=('public', 'optional')
    )


# 2ª segunda-feira de dezembro — início do período de recuperação
def segunda_segunda_dezembro(ano):
    d = date(ano, 12, 1)
    while d.weekday() != 0:
        d += timedelta(days=1)
    return d + timedelta(days=7)


def listar_recessos():
    return _carregar().get('recessos', [])


def listar_eventos():
    return _carregar().get('eventos', [])


def adicionar_recesso(data_iso, descricao):
    dados = _carregar()
    dados.setdefault('recessos', []).append(
        {'data': data_iso, 'descricao': descricao}
    )
    _salvar(dados)


def adicionar_evento(data_iso, descricao):
    dados = _carregar()
    dados.setdefault('eventos', []).append(
        {'data': data_iso, 'descricao': descricao}
    )
    _salvar(dados)


def remover_recesso(indice):
    dados = _carregar()
    dados['recessos'].pop(indice)
    _salvar(dados)


def remover_evento(indice):
    dados = _carregar()
    dados['eventos'].pop(indice)
    _salvar(dados)


# Classifica um dia em uma das categorias usadas para colorir o calendário.
# Precedência (de maior para menor): férias > feriado > evento > recesso >
# recuperação > fim de semana > letivo.
def status_do_dia(d: date):
    ano = d.year

    if d.month in (1, 7):
        return ('ferias', 'Férias')

    feriados = feriados_nacionais(ano)
    if d in feriados:
        return ('feriado', feriados.get(d))

    iso = d.isoformat()
    for ev in listar_eventos():
        if ev['data'] == iso:
            return ('evento', ev['descricao'])

    for r in listar_recessos():
        if r['data'] == iso:
            return ('recesso', r['descricao'])

    if (
        d.month == 12
        and d >= segunda_segunda_dezembro(ano)
        and d.weekday() < 5
    ):
        return ('recuperacao', 'Período de Recuperação')

    if d.weekday() >= 5:
        return ('fim_de_semana', 'Fim de semana')

    return ('letivo', 'Dia letivo')
