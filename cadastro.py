# =============================================================================
# UNICAMP — Universidade Estadual de Campinas
# Curso      : Data Science
# Disciplina : Aplicações em Data Science
# Professor  : Francisco Fambrini
#
# Aluno      : Edman Rodrigues Miranda
# RA         : 2026600198
# E-mail     : edmanrm@gmail.com
#
# Atividade  : Aula 1 — Cadastro de Pacientes
# Objetivo   : Desenvolver a mesma interface web em Gradio e Streamlit,
#              comparando as bibliotecas na prática e armazenando os
#              dados coletados em arquivo CSV.
#
# Campos     : Nome, idade, convênio, prioridade do atendimento e
#              motivo da consulta / observações.
# =============================================================================

"""Validação e persistência compartilhadas pelas duas interfaces."""
import csv
import math
from datetime import datetime
from pathlib import Path
from threading import Lock
from zoneinfo import ZoneInfo

import pandas as pd

COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]
_LOCK = Lock()


def criar_registro(nome, idade, convenio, prioridade, motivo):
    nome = str(nome or "").strip()
    motivo = str(motivo or "").strip()
    if not nome:
        raise ValueError("Informe o nome do paciente.")
    if len(nome) > 150 or len(motivo) > 2000:
        raise ValueError("Use até 150 caracteres no nome e 2.000 nas observações.")
    numeros = []
    for valor, campo, minimo, maximo in [(idade, "Idade", 0, 120), (prioridade, "Prioridade", 1, 5)]:
        try:
            numero = float(valor)
        except (TypeError, ValueError):
            raise ValueError(f"{campo}: informe um número inteiro entre {minimo} e {maximo}.") from None
        if not math.isfinite(numero) or not numero.is_integer() or not minimo <= numero <= maximo:
            raise ValueError(f"{campo}: informe um número inteiro entre {minimo} e {maximo}.")
        numeros.append(int(numero))
    if convenio not in CONVENIOS:
        raise ValueError("Selecione um convênio válido.")
    return dict(zip(COLUNAS, [datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d %H:%M:%S"), nome, numeros[0], convenio, numeros[1], motivo]))


def ler_registros(arquivo):
    arquivo = Path(arquivo)
    if not arquivo.exists() or arquivo.stat().st_size == 0:
        return pd.DataFrame(columns=COLUNAS)
    return pd.read_csv(arquivo, keep_default_na=False)


def salvar_registro(arquivo, registro):
    """Acrescenta uma linha; o cabeçalho é escrito apenas na criação."""
    arquivo = Path(arquivo)
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    with _LOCK:
        cabecalho = not arquivo.exists() or arquivo.stat().st_size == 0
        with arquivo.open("a", encoding="utf-8", newline="") as saida:
            writer = csv.DictWriter(saida, fieldnames=COLUNAS)
            if cabecalho:
                writer.writeheader()
            writer.writerow(registro)
        return ler_registros(arquivo)
