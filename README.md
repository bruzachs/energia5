# EnergIA 5.0: maturidade de empresas de energia sob a Indústria 5.0

Repositório da iniciação científica EnergIA 5.0 (PUC-Rio, Subprojeto WP2), orientada pelo Prof. Rodrigo G. G. Caiado. Reúne os dados, o código e a documentação do modelo de apoio à decisão multicritério que mede a maturidade de empresas de energia nas seis Dimensões Agregadas (DA-I a DA-VI) da taxonomia do artigo apresentado no ENEGEP 2026.

Bolsista: Bruna Zacharias.

## Estrutura

```
data/raw/         fontes originais, sem alteração
data/processed/   bases tratadas e versionadas (CSV)
src/              código reutilizável (carga de dados, TOPSIS)
notebooks/        análises, na ordem numérica
docs/             codebook, glossário e notas metodológicas
tests/            testes automáticos
```

## Como rodar

```bash
git clone <URL-DO-REPOSITORIO>
cd energia5
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab notebooks/00_inicio.ipynb
```

Nenhum arquivo externo é necessário: os dados usados pelo notebook inicial estão em `data/processed/`. Para rodar os testes: `pytest`.

## Dados

`data/processed/matriz_maturidade_v0.csv` tem 25 unidades empresa-ano (5 empresas, 2021 a 2025) com o percentual de maturidade em cada DA. É a versão v0, extraída dos relatórios de sustentabilidade e ainda sem evidência por célula (relatório, página e trecho). A v1 em formato longo, com evidência, é o próximo passo (ver `docs/`).

Limitações conhecidas da v0:
- as seis DAs não têm o mesmo número de indicadores, então os percentuais não são comparáveis entre dimensões (por exemplo, DA-VI usa denominador 3);
- algumas células foram estimadas por consistência aritmética, marcadas na coluna `observacoes`;
- os critérios de extração variaram entre relatórios (por exemplo, percentual de resíduos reciclados calculado a partir de dados brutos em um ano e marcado como não reportado em outro), o que cria variações artificiais, como a da Neoenergia entre 2022 e 2023.

Correções já feitas na auditoria de 06/10/2026 (detalhes em `docs/auditoria_matriz_v0.md`): Energisa 2024 DA-VI (0,75 para 1,00), Statkraft 2022 DA-III (0,25 para 0,75), Neoenergia 2022 DA-II (0,25 para 0,50) e Petrobras 2023 DA-III (0,75 para 1,00).

Ambas serão tratadas no codebook v1.

## Roteiro

1. Codebook de indicadores (`docs/codebook_v1.xlsx`, rascunho v1 com 24 indicadores, 4 por DA).
2. Base versionada com evidência por célula.
3. TOPSIS crisp (v0.1), depois Fuzzy-TOPSIS e pesos por BWM com especialistas.
4. Camada de explicação por IA generativa (QP3.1).

## Licença

Código sob licença MIT (ver `LICENSE`). Os dados derivam de relatórios públicos de sustentabilidade; cite a fonte original ao reutilizá-los.
