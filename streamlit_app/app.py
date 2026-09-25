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
#
# https://unicamp-cadastro-pacientes-tjyudzkkdcpdpryn7kwwm4.streamlit.app/
#
# =============================================================================

"""Execute: streamlit run streamlit_app/app.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import streamlit as st
from cadastro import COLUNAS, CONVENIOS, criar_registro, salvar_registro

st.set_page_config(page_title="Cadastro de pacientes", page_icon="🩺", layout="centered")
st.title("Cadastro de pacientes")
st.caption("Recepção do consultório · Atividade prática")
st.info("Demonstração acadêmica: utilize apenas dados fictícios.")

if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(columns=COLUNAS)
    # Cada sessão tem um arquivo separado, sem expor registros de outros visitantes.
    st.session_state.pasta_csv = tempfile.TemporaryDirectory(prefix="cadastro_pacientes_")
    st.session_state.arquivo_csv = str(Path(st.session_state.pasta_csv.name) / "pacientes.csv")

with st.form("cadastro", clear_on_submit=True):
    nome = st.text_input("Nome do paciente", placeholder="Digite o nome completo", max_chars=150)
    idade = st.number_input("Idade", min_value=0, max_value=120, value=0, step=1)
    convenio = st.selectbox("Convênio", CONVENIOS)
    prioridade = st.slider("Prioridade do atendimento", 1, 5, 1, help="1 = menor prioridade · 5 = urgente")
    motivo = st.text_area("Motivo da consulta / observações", max_chars=2000)
    enviado = st.form_submit_button("Cadastrar", type="primary", use_container_width=True)

if enviado:
    try:
        registro = criar_registro(nome, idade, convenio, prioridade, motivo)
        # Só atualiza a sessão após confirmar a escrita física do CSV.
        dados = salvar_registro(st.session_state.arquivo_csv, registro)
    except ValueError as erro:
        st.error(str(erro))
    except OSError:
        st.error("Não foi possível salvar o cadastro. Tente novamente.")
    else:
        st.session_state.pacientes = dados
        st.success("Paciente cadastrado com sucesso!")

st.subheader("Últimos 5 cadastros")
st.caption(f"Total nesta sessão: {len(st.session_state.pacientes)}")
st.dataframe(st.session_state.pacientes.tail(5), hide_index=True, use_container_width=True)
st.download_button("Baixar CSV", data=st.session_state.pacientes.to_csv(index=False).encode("utf-8-sig"), file_name="pacientes.csv", mime="text/csv", on_click="ignore", use_container_width=True)
st.caption("Baixe o CSV antes de sair. Os registros desta sessão não são permanentes; podem ser perdidos ao recarregar a página ou reiniciar o aplicativo.")
