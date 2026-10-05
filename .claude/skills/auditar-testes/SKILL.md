---
name: auditar-testes
description: Auditoria da suíte contra o PRD antes de declarar qualquer tarefa pronta. Use ao terminar uma regra, antes de commit, e quando o autor pedir para "auditar" ou "conferir os testes".
---

# Auditoria da suíte de testes

Rode cada passo e mostre a **saída real**. Não resuma o que "deveria" acontecer.

## 1. Execução

```bash
uv.exe run pytest -v
uv.exe run pytest --cov=app --cov-branch --cov-report=term-missing
```

- Todos os testes passam?
- `Cover` = 100% e `BrPart` = 0 em `app/situacao_academica.py`?
- A coluna `Missing` está vazia?

## 2. Rastreabilidade com o PRD

Para cada linha da **matriz de valores limite (PRD, seção 6.2)**, encontre o `id` do teste que
cobre **cada lado** da fronteira. Liste numa tabela `limite → ids`. Se faltar algum lado, é uma lacuna.

Faça o mesmo para as partições da seção 6.3 e os casos de Error Guessing da seção 6.4.

## 3. Viés de caminho feliz

IA tende a gerar valores "confortáveis" no meio da faixa. Procure:

- testes de limite que usam 5,0 em vez de 5,9 / 6,0;
- `parametrize` sem `ids` ou com `ids` sem prefixo `ep_` / `bva_` / `eg_`;
- `pytest.raises` sem `match=` (passaria com a exceção errada);
- asserts que comparam `float` com `Decimal`, ou que usam `pytest.approx` onde a igualdade deveria ser exata.

## 4. Forma dos testes

- Todo teste tem `@pytest.mark.unit` e os comentários `# Arrange`, `# Act` e `# Assert`?
- Algum teste depende de outro ou de ordem de execução?

## 5. Prova de que os testes pegam erro (mutação manual)

Escolha 2 limites e altere temporariamente o código, por exemplo `>=` para `>` em RN04 ou
`ROUND_HALF_UP` para `ROUND_HALF_EVEN`. Rode os testes, confirme que **algum falha** e reverta.
Cobertura de 100% só mostra que a linha rodou, não que o teste verificou algo.

## 6. Registro

Anote em `AI_USAGE.md` o que a auditoria encontrou e o que foi corrigido.
