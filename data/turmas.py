import streamlit as st

ANOS = ['1º ano', '2º ano', '3º ano']
CLASSES = ['Classe A', 'Classe B', 'Classe C']
TURNOS = ['Manhã', 'Tarde', 'Noite']

ALUNOS_POR_TURMA = {
    ('1º ano', 'Classe A', 'Manhã'): ['Ana Silva', 'Bruno Souza'],
    ('1º ano', 'Classe A', 'Tarde'): ['Carla Lima', 'Diego Rocha'],
    ('1º ano', 'Classe A', 'Noite'): ['Eduarda Alves', 'Felipe Costa'],
    ('1º ano', 'Classe B', 'Manhã'): ['Gabriela Dias', 'Henrique Melo'],
    ('1º ano', 'Classe B', 'Tarde'): ['Isabela Nunes', 'João Pereira'],
    ('1º ano', 'Classe B', 'Noite'): ['Karina Ramos', 'Lucas Teixeira'],
    ('1º ano', 'Classe C', 'Manhã'): ['Mariana Pinto', 'Nicolas Vieira'],
    ('1º ano', 'Classe C', 'Tarde'): ['Olivia Barros', 'Pedro Castro'],
    ('1º ano', 'Classe C', 'Noite'): ['Quenia Duarte', 'Rafael Esteves'],

    ('2º ano', 'Classe A', 'Manhã'): ['Sofia Farias', 'Thiago Gomes'],
    ('2º ano', 'Classe A', 'Tarde'): ['Ursula Henrique', 'Vitor Ibrahim'],
    ('2º ano', 'Classe A', 'Noite'): ['Wanda Junqueira', 'Xavier Klein'],
    ('2º ano', 'Classe B', 'Manhã'): ['Yasmin Lopes', 'Zeca Martins'],
    ('2º ano', 'Classe B', 'Tarde'): ['Alice Neves', 'Beto Oliveira'],
    ('2º ano', 'Classe B', 'Noite'): ['Camila Paiva', 'Daniel Queiroz'],
    ('2º ano', 'Classe C', 'Manhã'): ['Elisa Rangel', 'Fabio Santos'],
    ('2º ano', 'Classe C', 'Tarde'): ['Giovana Tavares', 'Hugo Ueda'],
    ('2º ano', 'Classe C', 'Noite'): ['Ines Vasques', 'Julio Werner'],

    ('3º ano', 'Classe A', 'Manhã'): ['Lara Xerez', 'Marcos Yamada'],
    ('3º ano', 'Classe A', 'Tarde'): ['Nayara Zaca', 'Otavio Abreu'],
    ('3º ano', 'Classe A', 'Noite'): ['Patricia Brito', 'Quincas Caldas'],
    ('3º ano', 'Classe B', 'Manhã'): ['Renata Diniz', 'Samuel Eulalio'],
    ('3º ano', 'Classe B', 'Tarde'): ['Tatiane Freitas', 'Ueslei Galvão'],
    ('3º ano', 'Classe B', 'Noite'): ['Valeria Horta', 'William Iglesias'],
    ('3º ano', 'Classe C', 'Manhã'): ['Xuxa Jardim', 'Yago Kruger'],
    ('3º ano', 'Classe C', 'Tarde'): ['Zilda Lacerda', 'Adriano Macedo'],
    ('3º ano', 'Classe C', 'Noite'): ['Beatriz Nogueira', 'Caio Ortiz'],
}


def selecionar_turma():
    col1, col2, col3 = st.columns(3)
    with col1:
        ano = st.selectbox('Ano:', ANOS)
    with col2:
        classe = st.selectbox('Classe:', CLASSES)
    with col3:
        turno = st.selectbox('Turno:', TURNOS)
    return ano, classe, turno


def alunos_da_turma(turma):
    return ALUNOS_POR_TURMA.get(turma, [])
