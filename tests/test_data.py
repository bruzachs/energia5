from src.data import load_matriz, DAS


def test_matriz_shape():
    df = load_matriz()
    assert len(df) == 25
    assert df["empresa"].nunique() == 5
    assert set(DAS) <= set(df.columns)


def test_valores_validos():
    df = load_matriz()
    assert df[DAS].min().min() >= 0
    assert df[DAS].max().max() <= 1
