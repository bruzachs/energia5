"""Carga e validação da matriz de maturidade."""
from pathlib import Path
import pandas as pd

DAS = ["DA_I", "DA_II", "DA_III", "DA_IV", "DA_V", "DA_VI"]
ROOT = Path(__file__).resolve().parents[1]
MATRIZ_V0 = ROOT / "data" / "processed" / "matriz_maturidade_v0.csv"


def load_matriz(path: Path = MATRIZ_V0) -> pd.DataFrame:
    """Lê a matriz e valida: valores em [0, 1], sem duplicatas empresa-ano."""
    df = pd.read_csv(path)
    if df[DAS].isna().any().any():
        raise ValueError("Há células vazias nas DAs")
    if ((df[DAS] < 0) | (df[DAS] > 1)).any().any():
        raise ValueError("Valores fora de [0, 1]")
    if df.duplicated(["empresa", "ano"]).any():
        raise ValueError("Pares empresa-ano duplicados")
    df["maturidade_media"] = df[DAS].mean(axis=1)
    return df
