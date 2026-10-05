# Relatório de transparência — uso de IA

## Ferramenta

| Item | Valor |
|---|---|
| Ferramenta | **Claude Code** (CLI da Anthropic), modelo Claude Opus 5.5 |
| Ambiente | WSL (Ubuntu) acessando o projeto no disco do Windows; testes executados com o `uv.exe` do Windows |
| Arquivos de contexto | `AGENTS.md` (regras gerais), `CLAUDE.md` (específico do Claude Code), `.claude/settings.json` (permissões) e `.claude/skills/auditar-testes/` (checklist de auditoria) |

## Como a IA foi empregada

| Etapa | Quem decidiu | Papel da IA |
|---|---|---|
| Escolha do tema | Autor | Propôs 4 temas com prós e contras; o autor escolheu "situação acadêmica" |
| Regras de negócio | Autor aprovou | Propôs enriquecer as regras (recuperação, conceito, validações) para ter partições e limites suficientes; o autor aprovou a versão fictícia |
| Decisão de arredondamento | Autor aprovou | Mostrou com saída real que `round(5.85, 1)` dá `5.8` e propôs `Decimal` com `ROUND_HALF_UP` |
| `PRD.md` e harness de IA | Autor revisou antes do código | Redigiu os arquivos; o autor revisou e aprovou antes de qualquer linha de código |
| Implementação e testes | IA, guiada pelo PRD | TDD em cada regra: teste escrito primeiro, visto falhando, código mínimo, teste passando, commit |
| Auditoria | IA, com evidência | Skill `auditar-testes` (abaixo) |

### Limites impostos à IA (harness)

- O `PRD.md` é a fonte da verdade. O `.claude/settings.json` **exige confirmação do autor** para
  editar o PRD, para impedir que a IA "ajuste a regra para o teste passar".
- `git push` é bloqueado para a IA no `settings.json`. O push é decisão do autor.
- Nada de `# pragma: no cover`, e o `fail_under = 100` não pode ser reduzido.

## Como foi feita a auditoria

### 1. Execução determinística

```bash
uv run pytest -v                                                  # 121 passed
uv run pytest --cov=app --cov-branch --cov-report=term-missing    # 100% instruções, 32/32 ramificações
uv run --with mypy python -m mypy --strict app tests              # Success: no issues found in 8 source files
```

### 2. Rastreabilidade PRD → testes

Cada linha da matriz de valores limite (PRD, seção 6.2) foi conferida com os `ids` dos testes,
nos dois lados de cada fronteira: nota (-0,1 · 0 · 0,1 · 9,9 · 10 · 10,1), frequência (74,99 / 75),
média (3,9 / 4,0 e 5,9 / 6,0), arredondamento (5,94 / 5,95), média final (5,9 / 6,0) e conceito
(7,4 / 7,5 e 8,9 / 9,0).

### 3. Teste de mutação manual

Cobertura de 100% só prova que cada linha **executou**, não que algum teste **verificou** o
resultado. Por isso foram inseridos 9 defeitos de propósito no código, um de cada vez, e a suíte
foi rodada contra cada um. Todos foram detectados:

| Defeito inserido | Testes que falharam |
|---|---|
| RN04: `media >= 6.0` vira `media > 6.0` | 2 |
| RN05: `media >= 4.0` vira `media > 4.0` | 1 |
| RN03: `frequencia < 75` vira `frequencia <= 75` | 1 |
| RN02: `ROUND_HALF_UP` vira `ROUND_HALF_EVEN` | 3 |
| RN01: `Decimal(str(valor))` vira `Decimal(valor)` | 10 |
| RN01: remove a checagem de `bool` | 4 |
| RN01: remove a checagem de número finito (NaN/inf) | 9 |
| RN08: `media >= 7.5` vira `media > 7.5` | 2 |
| RN07: não arredonda a média de entrada | 2 |

Os defeitos de RN03 e RN05 foram pegos por **um único teste** cada, justamente o do valor limite
(frequência 75 e média 4,0). Sem a Análise do Valor Limite, a cobertura seguiria em 100% e esses
bugs passariam.

### 4. Problemas encontrados e corrigidos

| # | Problema | Como foi detectado | Correção |
|---|---|---|---|
| 1 | `float` + `round()` reprovaria um aluno com média 5,95 (P1 = 5,8, P2 = 5,8, Trabalho = 6,3 dá `5.949999999999999` e arredonda para 5,9) | Busca exaustiva de entradas que caem nos limites de arredondamento, feita **antes** da implementação | `Decimal` + `ROUND_HALF_UP`, e conversão de `float` via `str()` |
| 2 | Comentário no código atribuía `round(5.85, 1) = 5.8` ao arredondamento do banqueiro. A causa real é a representação binária do float | Conferência do comentário no interpretador | Comentário corrigido para citar as duas causas, com exemplo de cada uma |
| 3 | 11 testes de exceção usavam `# Act / Assert` juntos, violando o AAA explícito exigido | Script de auditoria que analisa a AST de cada teste | Act e Assert separados; a mensagem passou a ser conferida por igualdade exata, mais rigorosa que `match=` |
| 4 | `mypy.exe` foi bloqueado pela política de Controle de Aplicativo do Windows (`os error 4551`) | Execução da verificação de tipos | Execução via `python -m mypy` |

## Revisão humana do código

Verifiquei se as funções e regras apresentadas em `app/situacao_academica.py` estão de acordo com o que foi proposto no PRD.md

Rodei a suite de testes e conferi a cobertura
