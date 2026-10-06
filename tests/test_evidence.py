import pandas as pd

from src.evidence import load_longa, validar, agregar_das, progresso


def test_base_vazia_tem_600_linhas_sem_erros():
    df = load_longa()
    assert len(df) == 600
    assert df["indicador"].nunique() == 24
    assert validar(df) == []


def test_nota_sem_evidencia_e_rejeitada():
    df = load_longa().head(2).copy()
    df.loc[df.index[0], "valor"] = 0.75
    erros = validar(df)
    assert any("sem pagina" in e for e in erros)
    assert any("sem trecho_literal" in e for e in erros)


def test_calculado_e_projeto_respeitam_tetos():
    df = load_longa().head(2).copy()
    a, b = df.index[0], df.index[1]
    for k in (a, b):
        df.loc[k, "pagina"] = "12"
        df.loc[k, "trecho_literal"] = "trecho"
        df.loc[k, "data_acesso"] = "2026-10-06"
    df.loc[a, "valor"] = 1.0
    df.loc[a, "calculado"] = "sim"
    df.loc[b, "valor"] = 0.75
    df.loc[b, "escopo"] = "projeto"
    erros = validar(df)
    assert any("calculado" in e for e in erros)
    assert any("projeto único" in e for e in erros)


def test_agregacao_exige_os_4_indicadores():
    df = load_longa()
    um = df[(df.empresa == "Energisa") & (df.ano == 2021) & (df.DA == "DA-I")].copy()
    um["valor"] = [0.5, 0.75, 1.0, 0.25]
    resto = df.drop(um.index)
    wide = agregar_das(pd.concat([um, resto]))
    linha = wide[(wide.empresa == "Energisa") & (wide.ano == 2021)].iloc[0]
    assert linha["DA-I"] == 0.625
    assert pd.isna(linha["DA-II"]) and pd.isna(linha["indice_I5"])


def test_progresso():
    p = progresso(load_longa())
    assert p.loc[1, "total"] == 200 and p.loc[2, "total"] == 400
