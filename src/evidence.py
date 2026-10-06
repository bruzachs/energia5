"""Base longa de evidência (v1): validação e agregação em DAs."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
LONGA_V1 = ROOT / "data" / "processed" / "matriz_maturidade_v1_longa.csv"
NIVEIS = {0.0, 0.25, 0.5, 0.75, 1.0}
DAS_V1 = ["DA-I", "DA-II", "DA-III", "DA-IV", "DA-V", "DA-VI"]
ESCOPOS = {"empresa", "grupo", "projeto", "segmento", "controladora"}


def load_longa(path: Path = LONGA_V1) -> pd.DataFrame:
    txt = ["calculado", "escopo", "relatorio_arquivo", "pagina", "trecho_literal",
           "data_acesso", "codificador", "observacao"]
    return pd.read_csv(path, dtype={c: "string" for c in txt})


def validar(df: pd.DataFrame) -> list[str]:
    """Devolve a lista de problemas (vazia = base consistente).

    Regras do codebook v1: valor em {0; 0,25; 0,5; 0,75; 1}; nota acima de 0
    exige página, trecho literal e data de acesso; valor calculado vale no
    máximo 0,75; projeto único vale no máximo 0,5; escopo, quando preenchido,
    deve ser um dos valores aceitos.
    """
    erros: list[str] = []
    ja = df[df["valor"].notna()]
    for i, r in ja.iterrows():
        rotulo = f"{r['empresa']} {r['ano']} {r['indicador']}"
        v = float(r["valor"])
        if v not in NIVEIS:
            erros.append(f"{rotulo}: valor {v} fora da escala")
            continue
        if v > 0:
            for col in ("pagina", "trecho_literal", "data_acesso"):
                if pd.isna(r[col]) or str(r[col]).strip() == "":
                    erros.append(f"{rotulo}: nota {v} sem {col}")
        if str(r.get("calculado", "")).strip().lower() in ("1", "sim", "true", "x") and v > 0.75:
            erros.append(f"{rotulo}: valor calculado não pode passar de 0,75")
        escopo = r.get("escopo")
        if isinstance(escopo, str) and escopo.strip():
            if escopo.strip() not in ESCOPOS:
                erros.append(f"{rotulo}: escopo '{escopo}' inválido")
            elif escopo.strip() == "projeto" and v > 0.5:
                erros.append(f"{rotulo}: projeto único não pode passar de 0,5")
    dup = df.duplicated(["empresa", "ano", "indicador"])
    if dup.any():
        erros.append(f"{int(dup.sum())} linhas duplicadas empresa-ano-indicador")
    return erros


def agregar_das(df: pd.DataFrame) -> pd.DataFrame:
    """Nota por DA (média dos 4 indicadores) e índice (média das 6 DAs).

    Só calcula a DA quando os 4 indicadores têm valor; caso contrário fica NaN.
    """
    d = df.copy()
    d["valor"] = pd.to_numeric(d["valor"], errors="coerce")
    g = d.groupby(["empresa", "ano", "DA"])["valor"]
    das = g.apply(lambda s: s.mean() if s.notna().sum() == 4 else float("nan"))
    wide = das.unstack("DA").reindex(columns=DAS_V1)
    wide["indice_I5"] = wide[DAS_V1].mean(axis=1, skipna=False)
    return wide.reset_index()


def progresso(df: pd.DataFrame) -> pd.DataFrame:
    """Células preenchidas por prioridade (1 = DA-I e DA-II)."""
    d = df.copy()
    d["preenchida"] = d["valor"].notna()
    t = d.groupby("prioridade")["preenchida"].agg(["sum", "count"])
    t["pct"] = (100 * t["sum"] / t["count"]).round(1)
    return t.rename(columns={"sum": "preenchidas", "count": "total"})
