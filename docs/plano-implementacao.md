# Plano de implementação — Motor de Situação Acadêmica

**Objetivo:** implementar as regras RN01 a RN08 do `PRD.md` com uma suíte Pytest que atinja
100% de cobertura de instruções e ramificações.

**Arquitetura:** um único módulo de domínio (`app/situacao_academica.py`) com uma função curta
por regra e um `StrEnum` para as situações. Um arquivo de teste por grupo de regras (PRD, seção 6.1).

**Stack:** Python 3.12+ (executado em 3.14) · uv · pytest · pytest-cov. Só biblioteca padrão no domínio.

**Spec:** `PRD.md` · **Contexto para IA:** `AGENTS.md`, `CLAUDE.md`

**Execução:** feita pelo próprio agente nesta sessão (TDD: teste falhando → código mínimo →
teste passando → commit), com a skill `auditar-testes` ao final.

## Restrições globais

- `requires-python = ">=3.12"`, sem dependências de produção.
- Mensagens de erro sem acento e com o nome do campo.
- Notas e médias em `Decimal`, com arredondamento `ROUND_HALF_UP` para 1 casa.
- Todo teste com `@pytest.mark.unit`, comentários AAA e `ids` com prefixo `ep_` / `bva_` / `eg_`.
- `fail_under = 100` e nenhum `# pragma: no cover`.

## Pontos de atenção na revisão

1. `NaN` precisa ser recusado **antes** da checagem de faixa, porque as duas comparações dão `False`.
2. `bool` precisa ser recusado **antes** de aceitar `int`.
3. Uma média recebida já não arredondada (5,95) precisa ser arredondada antes de entrar nas
   regras RN07 e RN08.
4. `Decimal("NaN")` e `Decimal("Infinity")` também precisam ser recusados, não só os de `float`.
5. Um `float` precisa virar `Decimal` via `str()`. `Decimal(5.85)` carrega o erro binário do float.

## Tarefas

### Tarefa 1 — Setup do projeto
- [x] `pyproject.toml` com markers, `--strict-markers` e coverage (`branch`, `fail_under = 100`)
- [x] `uv add --dev pytest pytest-cov`, `.python-version`, `.gitignore`
- [x] Repositório git e repositório privado no GitHub

### Tarefa 2 — RN01: validação (`tests/test_validacao.py`)
- [ ] Testes de BVA de nota (-0,1 · 0,0 · 0,1 · 9,9 · 10,0 · 10,1) e de frequência (-0,01 · 0 · 0,01 · 99,99 · 100 · 100,01)
- [ ] Testes de EP de tipo (`int`, `float`, `Decimal`) e de EG (`bool`, `str`, `None`, `list`, `nan`, `±inf`, `Decimal("NaN")`)
- [ ] Ver falhar → implementar `validar_nota`, `validar_frequencia` → ver passar → commit

### Tarefa 3 — RN02: média (`tests/test_media.py`)
- [ ] Testes de pesos, do arredondamento HALF_UP (5,94 → 5,9 · 5,95 → 6,0 · 5,85 → 5,9) e de propagação de erro de validação
- [ ] Ver falhar → implementar `calcular_media` → ver passar → commit

### Tarefa 4 — RN03 a RN06: situação (`tests/test_situacao.py`)
- [ ] EP das 4 situações; BVA de frequência 74,99 / 75 e de média 3,9 / 4,0 e 5,9 / 6,0; EG de falta com nota 10
- [ ] Ver falhar → implementar `Situacao` e `avaliar_situacao` → ver passar → commit

### Tarefa 5 — RN07: recuperação (`tests/test_recuperacao.py`)
- [ ] BVA da média final 5,9 / 6,0; EG de estado (média 3,9 e 6,0); arredondamento da média de entrada
- [ ] Ver falhar → implementar `calcular_media_final` e `avaliar_recuperacao` → ver passar → commit

### Tarefa 6 — RN08: conceito (`tests/test_conceito.py`)
- [ ] BVA 7,4 / 7,5 e 8,9 / 9,0; EP A/B/C/D; EG de `APROVADO` com média 5,0 e situação que não é `Situacao`
- [ ] Ver falhar → implementar `classificar_conceito` → ver passar → commit

### Tarefa 7 — Auditoria e documentação
- [ ] Rodar a skill `auditar-testes`, incluindo a mutação manual
- [ ] Escrever `AI_USAGE.md` e `README.md` com as evidências reais
- [ ] Commit e push
