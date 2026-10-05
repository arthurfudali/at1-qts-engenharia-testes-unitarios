# CLAUDE.md

@AGENTS.md
@PRD.md

## Específico do Claude Code neste ambiente

- O Claude Code roda no **WSL**, mas o projeto mora no disco do Windows e é executado pelo autor no
  PowerShell. Por isso use sempre o **`uv.exe`** (uv do Windows, já no PATH do WSL), nunca um `uv` Linux:
  um `.venv` criado pelo Linux quebra no Windows.
  ```bash
  uv.exe run pytest -v
  uv.exe run pytest --cov=app --cov-branch --cov-report=term-missing
  ```
- O interpretador é o `C:\Python314\python.exe`, fixado em `.python-version`. Existe um
  `python3.14.exe` do Chocolatey bloqueado por política de Controle de Aplicativo do Windows
  (erro `os error 4551`). Se o uv tentar usá-lo, o problema é a descoberta de interpretador,
  não o código.

## Fluxo de trabalho

1. Leia a regra no PRD antes de tocar no código.
2. Escreva o teste primeiro (TDD): veja-o falhar, implemente o mínimo, veja-o passar.
3. Rode a skill `auditar-testes` antes de dizer que algo está pronto.
4. Explique as decisões enquanto trabalha: qual era a alternativa e por que foi descartada.
