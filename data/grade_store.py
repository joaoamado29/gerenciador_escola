# Camada de dados da grade horária (persiste em data/grade.json)
import json
from pathlib import Path

# Disciplinas oferecidas pela escola
DISCIPLINAS = [
    'Português', 'Matemática', 'História', 'Geografia',
    'Física', 'Química', 'Biologia', 'Inglês',
    'Filosofia', 'Sociologia', 'Ed. Física', 'Artes',
]

# Turmas existentes (10 no total)
TURMAS = [
    '1º A', '1º B', '1º C', '1º D',
    '2º A', '2º B', '2º C',
    '3º A', '3º B', '3º C',
]

# Dias úteis e turnos disponíveis
DIAS = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
TURNOS = ['Manhã', 'Tarde']

# Slots de aula (sem o intervalo); cada slot = (hora_inicio, hora_fim)
HORARIOS_AULAS = {
    'Manhã': [
        ('07:00', '07:50'),
        ('07:50', '08:40'),
        ('08:40', '09:30'),
        ('09:50', '10:40'),
        ('10:40', '11:30'),
        ('11:30', '12:20'),
    ],
    'Tarde': [
        ('13:00', '13:50'),
        ('13:50', '14:40'),
        ('14:40', '15:30'),
        ('15:50', '16:40'),
        ('16:40', '17:30'),
        ('17:30', '18:20'),
    ],
}

# Intervalo por turno (entre a 3ª e a 4ª aula)
INTERVALO = {
    'Manhã': ('09:30', '09:50'),
    'Tarde': ('15:30', '15:50'),
}

# Distribuição inicial de turnos por turma (admin pode alterar depois)
_TURNO_PADRAO = {
    '1º A': 'Manhã', '1º B': 'Manhã', '1º C': 'Manhã', '1º D': 'Manhã',
    '2º A': 'Tarde', '2º B': 'Tarde', '2º C': 'Tarde',
    '3º A': 'Manhã', '3º B': 'Manhã', '3º C': 'Manhã',
}

# Arquivo onde a grade fica salva
_ARQUIVO = Path(__file__).parent / 'grade.json'


# Gera uma grade inicial variada para uma turma (round-robin sobre as disciplinas)
def _seed_grade(idx_turma):
    grade = {}
    cursor = idx_turma * 7
    for dia in DIAS:
        slots = []
        for _ in range(6):
            slots.append(DISCIPLINAS[cursor % len(DISCIPLINAS)])
            cursor += 1
        grade[dia] = slots
    return grade


# Monta o JSON inicial com todas as turmas e suas grades padrão
def _seed_inicial():
    return {
        turma: {
            'turno': _TURNO_PADRAO[turma],
            'grade': _seed_grade(idx),
        }
        for idx, turma in enumerate(TURMAS)
    }


# Garante que o arquivo exista; se não, cria com a grade-semente
def _carregar():
    if not _ARQUIVO.exists():
        _salvar(_seed_inicial())
    with _ARQUIVO.open(encoding='utf-8') as f:
        return json.load(f)


def _salvar(dados):
    with _ARQUIVO.open('w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


# Retorna o turno ('Manhã' / 'Tarde') de uma turma
def turno_da_turma(turma):
    return _carregar()[turma]['turno']


# Retorna a grade {dia: [6 disciplinas]} de uma turma
def grade_da_turma(turma):
    return _carregar()[turma]['grade']


# Atualiza uma única célula da grade (usada pelo admin)
def atualizar_aula(turma, dia, indice_aula, disciplina):
    dados = _carregar()
    dados[turma]['grade'][dia][indice_aula] = disciplina
    _salvar(dados)


# Troca o turno de uma turma (mantém as disciplinas, só muda os horários exibidos)
def atualizar_turno(turma, novo_turno):
    dados = _carregar()
    dados[turma]['turno'] = novo_turno
    _salvar(dados)


# Devolve as 6 aulas do dia já com horários: [{hora_inicio, hora_fim, disciplina}]
def aulas_do_dia(turma, dia):
    turno = turno_da_turma(turma)
    grade = grade_da_turma(turma)
    disciplinas = grade[dia]
    return [
        {'hora_inicio': h_ini, 'hora_fim': h_fim, 'disciplina': disciplinas[i]}
        for i, (h_ini, h_fim) in enumerate(HORARIOS_AULAS[turno])
    ]


# Lista todas as aulas de uma disciplina em um dia/turno específico
# Resultado: [{turma, hora_inicio, hora_fim, indice_aula}]
def aulas_do_professor(disciplina, dia, turno):
    dados = _carregar()
    resultado = []
    for turma in TURMAS:
        if dados[turma]['turno'] != turno:
            continue
        slots = HORARIOS_AULAS[turno]
        for i, materia in enumerate(dados[turma]['grade'][dia]):
            if materia == disciplina:
                resultado.append({
                    'turma': turma,
                    'hora_inicio': slots[i][0],
                    'hora_fim': slots[i][1],
                    'indice_aula': i + 1,
                })
    return resultado
