"""Motor de situação acadêmica.

As regras estão descritas no PRD.md; cada função indica a regra (RNxx) que implementa.
"""

from decimal import ROUND_HALF_UP, Decimal
from enum import StrEnum

Numero = int | float | Decimal

NOTA_MINIMA = Decimal("0")
NOTA_MAXIMA = Decimal("10")
FREQUENCIA_MINIMA = Decimal("0")
FREQUENCIA_MAXIMA = Decimal("100")

PESO_P1 = Decimal("0.35")
PESO_P2 = Decimal("0.35")
PESO_TRABALHO = Decimal("0.30")

UMA_CASA_DECIMAL = Decimal("0.1")

FREQUENCIA_MINIMA_PARA_APROVACAO = Decimal("75")
MEDIA_MINIMA_PARA_APROVACAO = Decimal("6.0")
MEDIA_MINIMA_PARA_RECUPERACAO = Decimal("4.0")


class Situacao(StrEnum):
    APROVADO = "APROVADO"
    RECUPERACAO = "RECUPERACAO"
    REPROVADO_POR_NOTA = "REPROVADO_POR_NOTA"
    REPROVADO_POR_FALTA = "REPROVADO_POR_FALTA"


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


def _arredondar_uma_casa(valor: Decimal) -> Decimal:
    """RN02: arredondamento escolar, meio para cima (5,85 -> 5,9 e 5,95 -> 6,0)."""
    # O round() nativo tem dois problemas aqui: opera sobre float (5.85 é guardado como
    # 5.8499..., então round(5.85, 1) dá 5.8) e empata para o par (round(0.25, 1) dá 0.2).
    return valor.quantize(UMA_CASA_DECIMAL, rounding=ROUND_HALF_UP)


def calcular_media(p1: Numero, p2: Numero, trabalho: Numero) -> Decimal:
    """RN02: média ponderada das três notas, arredondada para uma casa."""
    nota_p1 = validar_nota(p1, "P1")
    nota_p2 = validar_nota(p2, "P2")
    nota_trabalho = validar_nota(trabalho, "Trabalho")

    media_sem_arredondar = nota_p1 * PESO_P1 + nota_p2 * PESO_P2 + nota_trabalho * PESO_TRABALHO

    return _arredondar_uma_casa(media_sem_arredondar)


def _situacao_pela_media(media: Decimal) -> Situacao:
    """RN04 a RN06: classifica uma média já arredondada."""
    if media >= MEDIA_MINIMA_PARA_APROVACAO:
        return Situacao.APROVADO

    if media >= MEDIA_MINIMA_PARA_RECUPERACAO:
        return Situacao.RECUPERACAO

    return Situacao.REPROVADO_POR_NOTA


def avaliar_situacao(p1: Numero, p2: Numero, trabalho: Numero, frequencia: Numero) -> Situacao:
    """RN03 a RN06: situação do aluno a partir das notas e da frequência."""
    # Tudo é validado antes de decidir: uma nota inválida não pode ficar escondida
    # atrás de uma reprovação por falta.
    media = calcular_media(p1, p2, trabalho)
    frequencia_validada = validar_frequencia(frequencia)

    if frequencia_validada < FREQUENCIA_MINIMA_PARA_APROVACAO:
        return Situacao.REPROVADO_POR_FALTA

    return _situacao_pela_media(media)
