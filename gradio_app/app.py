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

"""Execute: python gradio_app/app.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gradio as gr
from cadastro import CONVENIOS, criar_registro, ler_registros, salvar_registro

ARQUIVO_CSV = Path(__file__).resolve().parent / "pacientes.csv"


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    try:
        registro = criar_registro(nome, idade, convenio, prioridade, motivo)
        dados = salvar_registro(ARQUIVO_CSV, registro)
    except ValueError as erro:
        return str(erro), ler_registros(ARQUIVO_CSV).tail(5)
    except OSError:
        return "Não foi possível salvar o CSV. Verifique a permissão da pasta e tente novamente.", gr.skip()
    return "Paciente cadastrado com sucesso!", dados.tail(5)


with gr.Blocks(title="Cadastro de pacientes", analytics_enabled=False) as demo:
    gr.Markdown("# Cadastro de pacientes\nRecepção do consultório · Atividade prática\n\nDemonstração acadêmica: utilize apenas dados fictícios.")
    with gr.Column():
        nome = gr.Textbox(label="Nome do paciente", placeholder="Digite o nome completo", max_length=150)
        idade = gr.Number(label="Idade", value=0, minimum=0, maximum=120, step=1)
        convenio = gr.Dropdown(CONVENIOS, value="Particular", label="Convênio")
        prioridade = gr.Slider(1, 5, value=1, step=1, label="Prioridade do atendimento", info="1 = menor prioridade · 5 = urgente")
        motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3, max_length=2000)
        botao = gr.Button("Cadastrar", variant="primary")
        status = gr.Textbox(label="Status", interactive=False)
        tabela = gr.Dataframe(value=ler_registros(ARQUIVO_CSV).tail(5), label="Últimos 5 cadastros", interactive=False)
    botao.click(cadastrar_paciente, [nome, idade, convenio, prioridade, motivo], [status, tabela], concurrency_limit=1)
    demo.load(lambda: ler_registros(ARQUIVO_CSV).tail(5), outputs=tabela)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", theme=gr.themes.Soft(primary_hue="teal"), css=".gradio-container {max-width: 760px !important; margin: auto !important;}")
