# Cadastro de pacientes — Gradio e Streamlit

Atividade prática de Aplicações em Data Science — UNICAMP.
As duas versões têm os mesmos campos: nome, idade, convênio, prioridade de 1 a 5 e motivo/observações. Cada cadastro inclui data e hora de São Paulo.

## Executar localmente

Use Python 3.12. Na pasta deste projeto:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python gradio_app/app.py
```

No Windows, ative com `.venv\Scripts\activate`. Abra o endereço local exibido no terminal. Para Streamlit, em outro terminal com o ambiente ativado:

```sh
streamlit run streamlit_app/app.py
```

## Funcionamento

- **Gradio:** formulário em coluna única com `gr.Blocks()`. O botão acrescenta uma linha em `gradio_app/pacientes.csv`, com cabeçalho apenas na criação. Mostra a confirmação e os cinco últimos cadastros. O arquivo permanece entre execuções locais.
- **Streamlit:** usa `st.form()` e mantém os cadastros em `st.session_state`. Cada sessão grava seu próprio arquivo temporário `pacientes.csv`, sem misturar visitantes. O botão de download exporta todos os registros da sessão. O armazenamento na nuvem é efêmero: exporte antes de sair.
- **Validações:** nome obrigatório; idade inteira de 0 a 120; convênio da lista; prioridade inteira de 1 a 5. Observações são opcionais. Campos de texto têm limites de tamanho.
- **Demonstração acadêmica:** os exemplos e testes usam somente dados fictícios. Este protótipo não deve receber dados reais de pacientes.

## Comparação prática

| Aspecto | Gradio | Streamlit |
|---|---|---|
| Construção | Componentes dentro de Blocks | Comandos de interface dentro de form |
| Envio | Evento do botão chama uma função | Submit reexecuta o script e processa o formulário |
| Estado | CSV local compartilhado pelo aplicativo | DataFrame próprio de cada sessão |
| Resultado | Retorno da função atualiza Status e Dataframe | Mensagem e tabela são renderizadas pelo script |
| Persistência | Arquivo local conservado após encerrar | Arquivo temporário e exportação para guardar os dados |
| Uso nesta atividade | Execução local | Publicação no Community Cloud |

## Publicar no Streamlit Community Cloud

1. Publique este projeto no GitHub, incluindo `gradio_app/`, `streamlit_app/`, `cadastro.py` e `requirements.txt`.
2. Entre em https://share.streamlit.io/ e crie um aplicativo a partir do repositório.
3. Selecione a branch `main` e o arquivo `streamlit_app/app.py`.
4. Nas opções avançadas, use Python 3.12. Não há credenciais a configurar.
5. Publique e teste um cadastro fictício e o download. Acesse o mesmo endereço no celular.

Documentação oficial: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## Entrega

A pasta `entrega/` reúne o CSV fictício, a captura local e o registro dos testes/links.

## Testes

```sh
pip install pytest
python -m pytest tests -q
```
