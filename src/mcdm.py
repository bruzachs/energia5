"""TOPSIS crisp (Hwang e Yoon, 1981) com normalização vetorial."""
from __future__ import annotations

import numpy as np
import pandas as pd


def topsis(X, weights=None, benefit=None, normalization: str = "vector") -> np.ndarray:
    """Coeficiente de proximidade relativa (0 a 1) de cada alternativa.

    X        matriz m x n (alternativas x critérios), valores numéricos.
    weights  vetor de n pesos; se None, pesos iguais. São normalizados para somar 1.
    benefit  vetor booleano de n posições; True = quanto maior, melhor (padrão);
             False = critério de custo.
    normalization  'vector' (padrão, norma euclidiana da coluna) ou 'minmax'.
    """
    X = np.asarray(X, dtype=float)
    if X.ndim != 2:
        raise ValueError("X deve ser uma matriz 2D")
    m, n = X.shape
    w = np.full(n, 1.0 / n) if weights is None else np.asarray(weights, dtype=float)
    if w.shape != (n,) or (w < 0).any() or w.sum() <= 0:
        raise ValueError("pesos inválidos")
    w = w / w.sum()
    b = np.ones(n, dtype=bool) if benefit is None else np.asarray(benefit, dtype=bool)
    if b.shape != (n,):
        raise ValueError("benefit deve ter n posições")

    if normalization == "vector":
        norms = np.sqrt((X ** 2).sum(axis=0))
        norms[norms == 0] = 1.0  # coluna toda zero: normalizada continua zero
        N = X / norms
    elif normalization == "minmax":
        rng = X.max(axis=0) - X.min(axis=0)
        rng[rng == 0] = 1.0
        N = (X - X.min(axis=0)) / rng
    else:
        raise ValueError("normalization deve ser 'vector' ou 'minmax'")
    V = N * w

    ideal = np.where(b, V.max(axis=0), V.min(axis=0))
    anti = np.where(b, V.min(axis=0), V.max(axis=0))
    d_pos = np.sqrt(((V - ideal) ** 2).sum(axis=1))
    d_neg = np.sqrt(((V - anti) ** 2).sum(axis=1))
    denom = d_pos + d_neg
    out = np.divide(d_neg, denom, out=np.full(m, 0.5), where=denom > 0)
    return out


def rank_table(df: pd.DataFrame, criteria: list[str], weights=None, benefit=None,
               id_cols: list[str] | None = None, normalization: str = "vector") -> pd.DataFrame:
    """Aplica o TOPSIS a um DataFrame e devolve o ranking (1 = melhor)."""
    res = df.copy()
    res["topsis"] = topsis(df[criteria].to_numpy(), weights, benefit, normalization)
    res["ranking"] = res["topsis"].rank(ascending=False, method="min").astype(int)
    cols = (id_cols or []) + criteria + ["topsis", "ranking"]
    return res[cols].sort_values("ranking")
