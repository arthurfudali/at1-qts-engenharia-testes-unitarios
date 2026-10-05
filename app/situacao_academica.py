"""Motor de situação acadêmica.

As regras estão descritas no PRD.md; cada função indica a regra (RNxx) que implementa.
"""

from decimal import Decimal

Numero = int | float | Decimal

NOTA_MINIMA = Decimal("0")
NOTA_MAXIMA = Decimal("10")
FREQUENCIA_MINIMA = Decimal("0")
FREQUENCIA_MAXIMA = Decimal("100")


def _converter_para_decimal(valor: Numero, nome_campo: str) -> Decimal:
    """RN01: aceita só int, float ou Decimal finitos e devolve um Decimal."""
    # bool é subclasse de int: sem esta checagem, True passaria como nota 1.
    if isinstance(valor, bool):
        raise TypeError(f"{nome_campo} deve ser numerico")

    if not isinstance(valor, (int, float, Decimal)):
        raise TypeError(f"{nome_campo} deve ser numerico")

    # Passar por str() evita que o Decimal herde o erro binário do float:
    # Decimal(5.85) é 5.8499999..., Decimal("5.85") é exatamente 5.85.
    valor_decimal = Decimal(str(valor))

    # NaN precisa ser barrado aqui: NaN < 0 e NaN > 10 são ambos falsos,
    # então ele passaria pela checagem de faixa.
    if not valor_decimal.is_finite():
        raise ValueError(f"{nome_campo} deve ser um numero finito")

    return valor_decimal


def validar_nota(valor: Numero, nome_campo: str) -> Decimal:
    """RN01: nota entre 0 e 10, inclusive."""
    nota = _converter_para_decimal(valor, nome_campo)

    if nota < NOTA_MINIMA or nota > NOTA_MAXIMA:
        raise ValueError(f"{nome_campo} deve estar entre 0 e 10")

    return nota


def validar_frequencia(frequencia: Numero) -> Decimal:
    """RN01: frequência entre 0 e 100, inclusive."""
    frequencia_decimal = _converter_para_decimal(frequencia, "Frequencia")

    if frequencia_decimal < FREQUENCIA_MINIMA or frequencia_decimal > FREQUENCIA_MAXIMA:
        raise ValueError("Frequencia deve estar entre 0 e 100")

    return frequencia_decimal
