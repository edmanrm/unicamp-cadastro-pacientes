# Entrega — Cadastro de pacientes

Repositório: https://github.com/edmanrm/unicamp-cadastro-pacientes

Aplicativo público: pendente de autenticação no Streamlit Community Cloud.

## Arquivos

- `gradio-local.png`: captura do Gradio executado localmente, com confirmação e registro fictício.
- `pacientes.csv`: exemplo gerado pelo formulário Gradio, com cabeçalho e data/hora.
- `streamlit-local.png`: captura do Streamlit local.
- `gradio-mobile.png` e `streamlit-mobile.png`: capturas em viewport de 390 × 844 pixels.

## Verificação realizada em 25/09/2026

- 11 testes automatizados aprovados (pytest e Streamlit AppTest).
- Gravação incremental, cabeçalho único, acentos, vírgulas, aspas e quebras de linha conferidos.
- Validação de nome obrigatório, idade, convênio e prioridade.
- Seis cadastros no Streamlit: seis registros persistidos e cinco exibidos.
- Segunda sessão sem acesso aos registros da primeira.
- Cadastro pelo navegador nas duas interfaces com confirmação.
- Botão Baixar CSV acionado no navegador e evento de download confirmado.
- Layout inspecionado em largura de celular (390 pixels).

O teste em celular físico e o teste da URL pública dependem da publicação. A simulação de tamanho de tela não substitui o teste no aparelho.
