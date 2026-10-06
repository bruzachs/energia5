import numpy as np
import pytest

from src.mcdm import topsis


def topsis_referencia(X, w, benefit):
    """Implementação independente, com laços, para conferir a vetorizada."""
    m, n = len(X), len(X[0])
    w = [wi / sum(w) for wi in w]
    norm = [sum(X[i][j] ** 2 for i in range(m)) ** 0.5 for j in range(n)]
    V = [[X[i][j] / norm[j] * w[j] for j in range(n)] for i in range(m)]
    ideal, anti = [], []
    for j in range(n):
        col = [V[i][j] for i in range(m)]
        ideal.append(max(col) if benefit[j] else min(col))
        anti.append(min(col) if benefit[j] else max(col))
    out = []
    for i in range(m):
        dp = sum((V[i][j] - ideal[j]) ** 2 for j in range(n)) ** 0.5
        dn = sum((V[i][j] - anti[j]) ** 2 for j in range(n)) ** 0.5
        out.append(dn / (dp + dn))
    return out


def test_dominancia():
    # A alternativa 2 domina a 1 em todos os critérios: C = 0 e 1
    c = topsis([[1, 2], [3, 4]])
    assert c == pytest.approx([0.0, 1.0])


def test_simetria():
    c = topsis([[1, 4], [4, 1]])
    assert c == pytest.approx([0.5, 0.5])


def test_confere_com_implementacao_independente():
    X = [[7, 9, 9, 8], [8, 7, 8, 7], [9, 6, 8, 9], [6, 7, 8, 6]]
    w = [0.1, 0.4, 0.3, 0.2]
    benefit = [True, True, False, True]
    esperado = topsis_referencia(X, w, benefit)
    assert topsis(X, w, benefit) == pytest.approx(esperado)


def test_invariante_a_escala_da_coluna():
    X = np.array([[3.0, 10.0], [5.0, 4.0], [4.0, 7.0]])
    Y = X.copy()
    Y[:, 1] *= 1000
    assert topsis(X) == pytest.approx(topsis(Y))


def test_criterio_de_custo_inverte_a_ordem():
    X = [[1, 5], [2, 5]]
    beneficio = topsis(X, benefit=[True, True])
    custo = topsis(X, benefit=[False, True])
    assert beneficio[1] > beneficio[0]
    assert custo[1] < custo[0]


def test_pesos_invalidos():
    with pytest.raises(ValueError):
        topsis([[1, 2], [3, 4]], weights=[1])


def test_minmax_dominancia_e_validacao():
    c = topsis([[1, 2], [3, 4]], normalization="minmax")
    assert c == pytest.approx([0.0, 1.0])
    with pytest.raises(ValueError):
        topsis([[1, 2], [3, 4]], normalization="outra")
