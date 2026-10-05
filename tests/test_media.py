"""RN02 — Média ponderada: P1 x 0,35 + P2 x 0,35 + Trabalho x 0,30 (PRD, seção 3)."""

from decimal import Decimal

import pytest

from app.situacao_academica import calcular_media


@pytest.mark.unit
@pytest.mark.parametrize(
    "p1, p2, trabalho, media_esperada",
    [
        (10, 0, 0, Decimal("3.5")),
        (0, 10, 0, Decimal("3.5")),
        (0, 0, 10, Decimal("3.0")),
        (0, 0, 0, Decimal("0.0")),
        (10, 10, 10, Decimal("10.0")),
        (7.0, 8.0, 6.0, Decimal("7.1")),
    ],
    ids=[
        "ep_peso_p1_35",
        "ep_peso_p2_35",
        "ep_peso_trabalho_30",
        "bva_todas_as_notas_minimas",
        "bva_todas_as_notas_maximas",
        "ep_notas_tipicas",
    ],
)
def test_calcular_media_aplica_os_pesos(
    p1: float, p2: float, trabalho: float, media_esperada: Decimal
) -> None:
    # Arrange
    notas = (p1, p2, trabalho)

    # Act
    media = calcular_media(*notas)

    # Assert
    assert media == media_esperada


@pytest.mark.unit
@pytest.mark.parametrize(
    "p1, p2, trabalho, media_esperada",
    [
        (6.0, 6.0, 5.8, Decimal("5.9")),
        (5.8, 5.8, 6.3, Decimal("6.0")),
        (5.7, 5.7, 6.2, Decimal("5.9")),
        (4.0, 4.0, 3.8, Decimal("3.9")),
        (3.8, 3.8, 4.3, Decimal("4.0")),
    ],
    ids=[
        "bva_media_bruta_5_94_arredonda_para_baixo",
        "bva_media_bruta_5_95_arredonda_para_cima",
        "eg_media_5_85_onde_round_nativo_daria_5_8",
        "bva_media_bruta_3_94_arredonda_para_baixo",
        "bva_media_bruta_3_95_arredonda_para_cima",
    ],
)
def test_calcular_media_arredonda_meio_para_cima(
    p1: float, p2: float, trabalho: float, media_esperada: Decimal
) -> None:
    # Arrange
    notas = (p1, p2, trabalho)

    # Act
    media = calcular_media(*notas)

    # Assert
    assert media == media_esperada


@pytest.mark.unit
def test_calcular_media_nao_sofre_imprecisao_de_float() -> None:
    # Arrange
    # Em float, 5.8*0.35 + 5.8*0.35 + 6.3*0.3 = 5.949999999999999 e round() daria 5.9,
    # mandando para a recuperação um aluno que tem média 6,0.
    p1, p2, trabalho = 5.8, 5.8, 6.3
    media_com_float = round(p1 * 0.35 + p2 * 0.35 + trabalho * 0.30, 1)

    # Act
    media = calcular_media(p1, p2, trabalho)

    # Assert
    assert media_com_float == 5.9
    assert media == Decimal("6.0")


@pytest.mark.unit
def test_calcular_media_devolve_uma_casa_decimal() -> None:
    # Arrange
    p1, p2, trabalho = 10, 10, 10

    # Act
    media = calcular_media(p1, p2, trabalho)

    # Assert
    assert str(media) == "10.0"


@pytest.mark.unit
@pytest.mark.parametrize(
    "p1, p2, trabalho, erro_esperado, mensagem",
    [
        (11, 5, 5, ValueError, "P1 deve estar entre 0 e 10"),
        (5, -1, 5, ValueError, "P2 deve estar entre 0 e 10"),
        (5, 5, None, TypeError, "Trabalho deve ser numerico"),
    ],
    ids=[
        "eg_p1_invalida_identifica_o_campo",
        "eg_p2_invalida_identifica_o_campo",
        "eg_trabalho_invalido_identifica_o_campo",
    ],
)
def test_calcular_media_valida_cada_nota(
    p1: object, p2: object, trabalho: object, erro_esperado: type[Exception], mensagem: str
) -> None:
    # Arrange
    notas = (p1, p2, trabalho)

    # Act / Assert
    with pytest.raises(erro_esperado, match=mensagem):
        calcular_media(*notas)  # type: ignore[arg-type]
