# AT1 — Engenharia de Testes Unitários e Cobertura de Código

Motor de **situação acadêmica** em Python. A partir de duas provas, um trabalho e a frequência,
ele decide se o aluno foi aprovado, está em recuperação ou foi reprovado, e atribui um conceito.
Atividade avaliativa da disciplina Qualidade e Teste de Software (FATEC).

| Documento | Conteúdo |
|---|---|
| [`PRD.md`](PRD.md) | Regras de negócio RN01 a RN08 e estratégia de testes |
| [`AGENTS.md`](AGENTS.md) | Regras de contexto para agentes de IA |
| [`CLAUDE.md`](CLAUDE.md) e [`.claude/`](.claude/) | Harness específico do Claude Code: permissões e skill de auditoria |
| [`AI_USAGE.md`](AI_USAGE.md) | Relatório de transparência do uso de IA |
| [`docs/plano-implementacao.md`](docs/plano-implementacao.md) | Plano de implementação seguido |

## Como rodar

Requer [uv](https://docs.astral.sh/uv/) e Python 3.12 ou superior.

```bash
uv sync
uv run pytest -v
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```

Só os testes unitários (todos são marcados):

```bash
uv run pytest -m unit -v
```

## Resultado

```
============================= 121 passed in 0.16s =============================
Name                        Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------
app\__init__.py                 0      0      0      0   100%
app\situacao_academica.py      90      0     32      0   100%
-----------------------------------------------------------------------
TOTAL                          90      0     32      0   100%
Required test coverage of 100.0% reached. Total coverage: 100.00%
```

O `pyproject.toml` define `fail_under = 100`. Se a cobertura cair, o comando falha.

## Estrutura

```
app/situacao_academica.py    domínio: uma função por regra de negócio
tests/test_validacao.py      RN01  validação de tipos, faixas, NaN, infinito e bool
tests/test_media.py          RN02  média ponderada e arredondamento
tests/test_situacao.py       RN03–RN06  falta, aprovação, recuperação e reprovação
tests/test_recuperacao.py    RN07  resultado da recuperação
tests/test_conceito.py       RN08  conceito A, B, C ou D
```

## Técnicas de teste

O `id` de cada caso parametrizado começa pela técnica aplicada, o que deixa a técnica visível
na saída do `pytest -v`:

| Prefixo | Técnica | Casos |
|---|---|---|
| `bva_` | Análise do Valor Limite | 50 |
| `eg_` | Error Guessing | 46 |
| `ep_` | Particionamento de Equivalência | 19 |

Mais 6 testes não parametrizados, num total de **121 casos em 31 funções de teste**, todos
com `@pytest.mark.unit` e com os comentários `# Arrange`, `# Act` e `# Assert`.

### O caso que justifica o `Decimal`

Com P1 = 5,8, P2 = 5,8 e Trabalho = 6,3, a média exata é 5,95. Pelo arredondamento escolar ela
vira 6,0, e o aluno é **aprovado**. Em `float`, a mesma conta dá `5.949999999999999`, e o
`round()` devolve 5,9: o aluno iria **para a recuperação**. O teste
`test_calcular_media_nao_sofre_imprecisao_de_float` documenta esse comportamento.
