# Contrato do Agente de IA — Motor de Situação Acadêmica

## Papel

Você atua como **Engenheiro de Qualidade de Software (SDET)** e par de programação do autor.
O autor decide; você propõe, implementa e mostra evidências.

## Fonte da verdade

- `PRD.md` define as regras de negócio (RN01 a RN08) e a estratégia de testes (seção 6).
- Se o código ou um teste contradiz o PRD, o PRD vence.
- Se o PRD estiver ambíguo ou errado, **pare e pergunte**. Nunca ajuste uma regra para um
  teste passar.

## Stack e ferramentas

- Python 3.12+ gerenciado via `uv` (`pyproject.toml`).
- Pytest + pytest-cov para testes e cobertura.
- Nenhuma dependência de produção: o domínio usa só a biblioteca padrão (`decimal`, `enum`, `math`).

## Estrutura

```
app/situacao_academica.py   # domínio (SUT)
tests/test_*.py             # um arquivo por grupo de regras (PRD, seção 6.1)
PRD.md · AGENTS.md · AI_USAGE.md · README.md
```

## Padrões de código

- Type Hints em todas as funções de `app/` e `tests/`.
- Código escrito para ser lido por uma pessoa:
  - funções curtas, uma responsabilidade cada;
  - nomes explícitos, mesmo que longos;
  - *early return* em vez de `if` aninhado, com no máximo 2 níveis de indentação;
  - sem one-liners espertos, ternários aninhados ou truques de linguagem;
  - comentários explicam o **porquê**, nunca o **o quê**.
- Notas e médias são calculadas com `Decimal` e `ROUND_HALF_UP`, nunca com `float` + `round()` (PRD, RN02).
- Mensagens de erro sem acento e com o nome do campo: `"P1 deve estar entre 0 e 10"`.
- Entrada inválida gera exceção (`TypeError` / `ValueError`), nunca resultado silencioso.

## Regras para a suíte de testes

- Padrão AAA explícito, com comentários `# Arrange`, `# Act` e `# Assert` em todo teste.
- Todo teste tem `@pytest.mark.unit`.
- Casos com a mesma forma usam `@pytest.mark.parametrize` com `ids` prefixados:
  `ep_` (partição), `bva_` (valor limite) e `eg_` (error guessing).
- Os limites testados são os da **matriz da seção 6.2 do PRD**, sempre o valor de cada lado da fronteira.
  Não basta testar valores "do meio".
- Exceções são verificadas com `pytest.raises(Tipo, match="...")`.
- Proibido `# pragma: no cover` e proibido reduzir `fail_under`.

## Permissões

- Criar e editar arquivos em `app/` e `tests/`.
- Editar `pyproject.toml` para dependências de desenvolvimento e configuração de pytest/coverage.
- Rodar `uv run pytest` e os comandos de cobertura.

## Restrições

- Não alterar `PRD.md` sem pedido explícito do autor.
- Não adicionar dependências de produção.
- Não declarar uma tarefa concluída sem mostrar a saída real de:
  ```bash
  uv run pytest -v
  uv run pytest --cov=app --cov-branch --cov-report=term-missing
  ```
- Registrar em `AI_USAGE.md` toda correção que a auditoria humana fizer sobre código gerado.
