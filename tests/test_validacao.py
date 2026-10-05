"""RN01 — Validação das entradas numéricas (PRD, seção 3)."""

from decimal import Decimal

import pytest

from app.situacao_academica import validar_frequencia, validar_nota


# ---------------------------------------------------------------------------
# Nota: valores aceitos
# ---------------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.parametrize(
    "nota, esperado",
    [
        (0.0, Decimal("0.0")),
        (0.1, Decimal("0.1")),
        (9.9, Decimal("9.9")),
        (10.0, Decimal("10.0")),
        (7.5, Decimal("7.5")),
        (8, Decimal("8")),
        (Decimal("6.5"), Decimal("6.5")),
    ],
    ids=[
        "bva_nota_0_minimo",
        "bva_nota_0_1_acima_do_minimo",
        "bva_nota_9_9_abaixo_do_maximo",
        "bva_nota_10_maximo",
        "ep_nota_float_no_meio",
        "ep_nota_int",
        "ep_nota_decimal",
    ],
)
def test_validar_nota_aceita_valores_validos(nota: float, esperado: Decimal) -> None:
    # Arrange
    nome_campo = "P1"

    # Act
    resultado = validar_nota(nota, nome_campo)

    # Assert
    assert resultado == esperado
    assert isinstance(resultado, Decimal)


@pytest.mark.unit
def test_validar_nota_converte_float_sem_carregar_erro_binario() -> None:
    # Arrange
    # Decimal(5.85) seria 5.8499999999999996447..., o que estragaria o arredondamento da RN02.
    nota_float = 5.85

    # Act
    resultado = validar_nota(nota_float, "P1")

    # Assert
    assert resultado == Decimal("5.85")


# ---------------------------------------------------------------------------
# Nota: valores fora da faixa
# ---------------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.parametrize(
    "nota",
    [-0.1, 10.1, -5, 50],
    ids=[
        "bva_nota_menos_0_1_abaixo_do_minimo",
        "bva_nota_10_1_acima_do_maximo",
        "ep_nota_negativa",
        "ep_nota_muito_alta",
    ],
)
def test_validar_nota_recusa_valor_fora_da_faixa(nota: float) -> None:
    # Arrange
    nome_campo = "P2"

    # Act
    with pytest.raises(ValueError) as erro:
        validar_nota(nota, nome_campo)

    # Assert
    assert str(erro.value) == "P2 deve estar entre 0 e 10"


# ---------------------------------------------------------------------------
# Nota: error guessing
# ---------------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.parametrize(
    "valor",
    ["7.5", None, [7.5], True, False],
    ids=[
        "eg_texto_numerico",
        "eg_none",
        "eg_lista",
        "eg_bool_true_seria_1",
        "eg_bool_false_seria_0",
    ],
)
def test_validar_nota_recusa_tipo_invalido(valor: object) -> None:
    # Arrange
    nome_campo = "Trabalho"

    # Act
    with pytest.raises(TypeError) as erro:
        validar_nota(valor, nome_campo)  # type: ignore[arg-type]

    # Assert
    assert str(erro.value) == "Trabalho deve ser numerico"


@pytest.mark.unit
@pytest.mark.parametrize(
    "valor",
    [float("nan"), float("inf"), float("-inf"), Decimal("NaN"), Decimal("Infinity")],
    ids=[
        "eg_nan_fura_checagem_de_faixa",
        "eg_infinito_positivo",
        "eg_infinito_negativo",
        "eg_decimal_nan",
        "eg_decimal_infinito",
    ],
)
def test_validar_nota_recusa_valor_nao_finito(valor: float) -> None:
    # Arrange
    nome_campo = "P1"

    # Act
    with pytest.raises(ValueError) as erro:
        validar_nota(valor, nome_campo)

    # Assert
    assert str(erro.value) == "P1 deve ser um numero finito"


# ---------------------------------------------------------------------------
# Frequência
# ---------------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.parametrize(
    "frequencia, esperado",
    [
        (0, Decimal("0")),
        (0.01, Decimal("0.01")),
        (99.99, Decimal("99.99")),
        (100, Decimal("100")),
        (80.5, Decimal("80.5")),
    ],
    ids=[
        "bva_frequencia_0_minimo",
        "bva_frequencia_0_01_acima_do_minimo",
        "bva_frequencia_99_99_abaixo_do_maximo",
        "bva_frequencia_100_maximo",
        "ep_frequencia_no_meio",
    ],
)
def test_validar_frequencia_aceita_valores_validos(frequencia: float, esperado: Decimal) -> None:
    # Arrange
    entrada = frequencia

    # Act
    resultado = validar_frequencia(entrada)

    # Assert
    assert resultado == esperado


@pytest.mark.unit
@pytest.mark.parametrize(
    "frequencia",
    [-0.01, 100.01],
    ids=[
        "bva_frequencia_menos_0_01_abaixo_do_minimo",
        "bva_frequencia_100_01_acima_do_maximo",
    ],
)
def test_validar_frequencia_recusa_valor_fora_da_faixa(frequencia: float) -> None:
    # Arrange
    entrada = frequencia

    # Act
    with pytest.raises(ValueError) as erro:
        validar_frequencia(entrada)

    # Assert
    assert str(erro.value) == "Frequencia deve estar entre 0 e 100"


@pytest.mark.unit
@pytest.mark.parametrize(
    "valor, erro_esperado, mensagem",
    [
        ("80", TypeError, "Frequencia deve ser numerico"),
        (True, TypeError, "Frequencia deve ser numerico"),
        (float("nan"), ValueError, "Frequencia deve ser um numero finito"),
    ],
    ids=[
        "eg_frequencia_texto",
        "eg_frequencia_bool",
        "eg_frequencia_nan",
    ],
)
def test_validar_frequencia_recusa_entrada_suspeita(
    valor: object, erro_esperado: type[Exception], mensagem: str
) -> None:
    # Arrange
    entrada = valor

    # Act
    with pytest.raises(erro_esperado) as erro:
        validar_frequencia(entrada)  # type: ignore[arg-type]

    # Assert
    assert str(erro.value) == mensagem
