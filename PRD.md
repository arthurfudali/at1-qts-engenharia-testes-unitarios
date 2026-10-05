# PRD — Motor de Situação Acadêmica

> Regulamento **fictício**, criado para a AT1 de Qualidade e Teste de Software.
> Ele não reproduz as regras oficiais da FATEC: foi enriquecido de propósito para ter
> partições e valores limite suficientes para uma suíte de testes completa.

## 1. Objetivo

Dado o desempenho de um aluno em uma disciplina (duas provas, um trabalho e a frequência),
o sistema deve:

1. validar as entradas;
2. calcular a média ponderada;
3. decidir a situação do aluno (aprovado, recuperação, reprovado por nota ou por falta);
4. calcular o resultado da recuperação, quando houver;
5. atribuir um conceito (A, B, C ou D).

O sistema é uma biblioteca Python pura, sem interface, banco de dados ou rede. Todas as
regras são determinísticas: a mesma entrada sempre produz a mesma saída.

## 2. Glossário

| Termo | Significado |
|---|---|
| P1, P2 | Notas das duas provas |
| Trabalho | Nota do trabalho da disciplina |
| Frequência | Percentual de presença do aluno, de 0 a 100 |
| Média | Média ponderada de P1, P2 e Trabalho, já arredondada (RN02) |
| Nota de recuperação | Nota da prova de recuperação, que só existe para quem está em recuperação |
| Média final | Média após a recuperação (RN07) |

## 3. Regras de negócio

### RN01 — Validação das entradas numéricas

Valem para P1, P2, Trabalho, Nota de recuperação, Média e Frequência.

| Situação da entrada | Resultado |
|---|---|
| Tipo diferente de `int`, `float` ou `Decimal` (ex.: `str`, `None`, `list`) | `TypeError` |
| Valor booleano (`True` / `False`) | `TypeError`, porque em Python `bool` é subclasse de `int` e passaria como 1 ou 0 |
| `NaN`, `inf` ou `-inf` | `ValueError` |
| Nota fora do intervalo **0,0 a 10,0** (inclusive) | `ValueError` |
| Frequência fora do intervalo **0 a 100** (inclusive) | `ValueError` |

- Texto numérico como `"7.5"` **não** é convertido. Coerção silenciosa esconde erros de quem chama.
- As mensagens de erro identificam o campo, por exemplo `"P1 deve estar entre 0 e 10"`.
- As mensagens não têm acento, seguindo o padrão usado em aula.

### RN02 — Média ponderada

```
média = P1 × 0,35 + P2 × 0,35 + Trabalho × 0,30
```

- O cálculo usa `Decimal`, não `float`. Exemplo do problema: em `float`,
  `0.35*6 + 0.35*6 + 0.3*5.8` dá `5.9399999999999995`.
- A média é arredondada para **1 casa decimal**, com arredondamento *meio para cima*
  (`ROUND_HALF_UP`): 5,85 vira 5,9 e 5,95 vira 6,0.
- Não se usa o `round()` nativo, porque `round(5.85, 1)` devolve `5.8`.
- **Todas as comparações com limites (RN04 a RN08) usam a média já arredondada.**

### RN03 — Reprovação por falta (prevalece sobre a nota)

- Frequência **< 75** → `REPROVADO_POR_FALTA`, qualquer que seja a média.
- A frequência **não** é arredondada: 74,99 reprova e 75 passa para a análise de nota.

### RN04 — Aprovação

- Frequência ≥ 75 e média ≥ **6,0** → `APROVADO`.

### RN05 — Recuperação

- Frequência ≥ 75 e **4,0 ≤ média < 6,0** → `RECUPERACAO`.

### RN06 — Reprovação por nota

- Frequência ≥ 75 e média < **4,0** → `REPROVADO_POR_NOTA`.

### RN07 — Resultado da recuperação

```
média final = (média + nota de recuperação) / 2
```

- A média final é arredondada como na RN02 (1 casa, `ROUND_HALF_UP`).
- Média final ≥ **6,0** → `APROVADO`. Abaixo disso → `REPROVADO_POR_NOTA`.
- Só pode ser calculado para quem está em recuperação, ou seja, com 4,0 ≤ média < 6,0.
  Fora dessa faixa → `ValueError("Aluno nao esta em recuperacao")`.
- A média e a nota de recuperação passam pela validação da RN01.
- A média recebida é arredondada como na RN02 antes de comparar com a faixa. Assim, quem
  chama com 5,95 recebe o mesmo tratamento de quem chama com 6,0, que não está em recuperação.

### RN08 — Conceito

| Situação | Média (ou média final) | Conceito |
|---|---|---|
| `APROVADO` | ≥ 9,0 | A |
| `APROVADO` | 7,5 ≤ média < 9,0 | B |
| `APROVADO` | 6,0 ≤ média < 7,5 | C |
| Qualquer outra | qualquer | D |

- Se a situação for `APROVADO` com média < 6,0, os dados são contraditórios →
  `ValueError("Media incompativel com situacao APROVADO")`.
- Uma situação que não seja membro de `Situacao` → `TypeError`.
- A média recebida passa pela RN01 e é arredondada como na RN02 antes das comparações.

### Ordem de avaliação

1. Valida todas as entradas (RN01). O primeiro campo inválido interrompe com erro.
2. Verifica a frequência (RN03).
3. Calcula a média (RN02).
4. Classifica na ordem: aprovado (RN04) → recuperação (RN05) → reprovado por nota (RN06).

## 4. Interface pública (módulo `app/situacao_academica.py`)

```python
Numero = int | float | Decimal

class Situacao(StrEnum):
    APROVADO, RECUPERACAO, REPROVADO_POR_NOTA, REPROVADO_POR_FALTA

validar_nota(valor: Numero, nome_campo: str) -> Decimal                # RN01
validar_frequencia(frequencia: Numero) -> Decimal                      # RN01
calcular_media(p1: Numero, p2: Numero, trabalho: Numero) -> Decimal    # RN02
avaliar_situacao(p1, p2, trabalho, frequencia) -> Situacao            # RN03–RN06
calcular_media_final(media: Numero, nota_recuperacao: Numero) -> Decimal  # RN07
avaliar_recuperacao(media: Numero, nota_recuperacao: Numero) -> Situacao  # RN07
classificar_conceito(media: Numero, situacao: Situacao) -> str         # RN08
```

## 5. Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF01 | Python 3.12+, projeto gerenciado com `uv` (`pyproject.toml`) |
| RNF02 | Type Hints em todas as funções de `app/` e `tests/` |
| RNF03 | Tratamento defensivo: nenhuma entrada inválida produz resultado silenciosamente errado |
| RNF04 | Código legível: funções curtas, nomes explícitos, *early return*, comentários só para explicar o "porquê" |

## 6. Estratégia de testes

### 6.1 Organização

| Arquivo | Regras |
|---|---|
| `tests/test_validacao.py` | RN01 |
| `tests/test_media.py` | RN02 |
| `tests/test_situacao.py` | RN03 a RN06 |
| `tests/test_recuperacao.py` | RN07 |
| `tests/test_conceito.py` | RN08 |

- Todo teste segue o padrão **AAA**, com comentários `# Arrange`, `# Act` e `# Assert`.
- Todo teste tem `@pytest.mark.unit`.
- Casos com a mesma forma usam `@pytest.mark.parametrize` com `ids` prefixados pela técnica:
  - `ep_` para Particionamento de Equivalência;
  - `bva_` para Análise do Valor Limite;
  - `eg_` para Error Guessing.
- Erros são verificados em dois passos AAA. No *Act*, `with pytest.raises(Tipo) as erro:` confere
  o tipo da exceção. No *Assert*, `assert str(erro.value) == "mensagem"` confere a mensagem por
  igualdade exata, que é mais rigorosa que a busca por regex do `match=`.

### 6.2 Matriz de valores limite (BVA)

Passo de 0,1 para notas e de 0,01 para frequência.

| Variável | Inválido abaixo | Limite | Transição | Limite | Inválido acima |
|---|---|---|---|---|---|
| Nota (RN01) | -0,1 | 0,0 / 0,1 | — | 9,9 / 10,0 | 10,1 |
| Frequência (RN01) | -0,01 | 0 / 0,01 | — | 99,99 / 100 | 100,01 |
| Frequência (RN03) | — | 74,99 → falta | | 75,00 → avalia nota | — |
| Média: reprovado ↔ recuperação | — | 3,9 → reprovado | | 4,0 → recuperação | — |
| Média: recuperação ↔ aprovado | — | 5,9 → recuperação | | 6,0 → aprovado | — |
| Arredondamento (RN02) | — | 5,94 → 5,9 | | 5,95 → 6,0 | — |
| Média final (RN07) | — | 5,9 → reprovado | | 6,0 → aprovado | — |
| Conceito C ↔ B | — | 7,4 → C | | 7,5 → B | — |
| Conceito B ↔ A | — | 8,9 → B | | 9,0 → A | — |

### 6.3 Partições de equivalência (EP)

| Variável | Partições |
|---|---|
| Situação | aprovado · recuperação · reprovado por nota · reprovado por falta |
| Conceito | A · B · C · D (não aprovado) |
| Tipo da entrada | numérico válido (`int`, `float`, `Decimal`) · não numérico · booleano |

### 6.4 Error Guessing (casos que um teste "caminho feliz" não pega)

| Entrada | Por que é suspeita |
|---|---|
| `True`, `False` | `bool` é `int` em Python |
| `float("nan")` | `nan < 0` e `nan > 10` são **ambos** falsos e furam a checagem de faixa |
| `float("inf")`, `float("-inf")`, `Decimal("NaN")` | não são números finitos |
| `"7.5"`, `None`, `[]` | tipos errados que chegam de formulário ou JSON |
| média 5,85 | o `round()` nativo erra o arredondamento |
| frequência 10 com notas 10 | a falta precisa prevalecer |
| recuperação com média 7,0 ou 3,0 | erro de estado |
| `APROVADO` com média 5,0 | dados contraditórios |

### 6.5 Critério de aceite

```bash
uv run pytest -v
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```

- Todos os testes passam.
- **100% de instruções e 100% de ramificações** em `app/`, garantido por `fail_under = 100`
  no `pyproject.toml`.
- Nenhum `# pragma: no cover`. Se uma linha não pode ser coberta, ela não deveria existir.
