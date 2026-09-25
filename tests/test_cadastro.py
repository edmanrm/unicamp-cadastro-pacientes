from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import pytest
from cadastro import criar_registro, salvar_registro
from streamlit.testing.v1 import AppTest


def test_csv_append_e_acentos(tmp_path):
    arquivo = tmp_path / "pacientes.csv"
    for nome in ["Paciente fictício A", "Paciente fictício B"]:
        salvar_registro(arquivo, criar_registro(nome, 32, "Unimed", 2, 'Observação, com vírgula e "aspas"\nsegunda linha'))
    df = pd.read_csv(arquivo)
    assert len(df) == 2
    assert df.nome.tolist() == ["Paciente fictício A", "Paciente fictício B"]
    assert df.motivo.iloc[0] == 'Observação, com vírgula e "aspas"\nsegunda linha'
    assert arquivo.read_text().count("timestamp,nome,idade,convenio,prioridade,motivo") == 1


@pytest.mark.parametrize("campo,valor", [(0, "  "), (1, -1), (1, 121), (1, 3.5), (1, None), (1, float("nan")), (2, "Inválido"), (3, 0), (3, 6)])
def test_validacao(campo, valor):
    dados = ["Paciente fictício", 32, "Particular", 1, ""]
    dados[campo] = valor
    with pytest.raises(ValueError):
        criar_registro(*dados)


def test_streamlit_fluxo_e_isolamento():
    app = str(Path(__file__).resolve().parents[1] / "streamlit_app/app.py")
    at = AppTest.from_file(app).run()
    assert not at.exception
    at.button[0].click().run()
    assert at.error and len(at.session_state.pacientes) == 0
    for i in range(6):
        at.text_input[0].set_value(f"Paciente fictício {i}")
        at.number_input[0].set_value(30+i)
        at.text_area[0].set_value("Cadastro de teste")
        at.button[0].click().run()
        assert not at.exception
        assert at.success
    assert len(at.session_state.pacientes) == 6
    assert len(at.dataframe[0].value) == 5
    assert len(pd.read_csv(at.session_state.arquivo_csv)) == 6
    outra = AppTest.from_file(app).run()
    assert len(outra.session_state.pacientes) == 0
    assert outra.session_state.arquivo_csv != at.session_state.arquivo_csv
