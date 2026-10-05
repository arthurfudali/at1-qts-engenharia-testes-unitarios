"""RN08 — Conceito A, B, C ou D (PRD, seção 3)."""

import pytest

from app.situacao_academica import Situacao, classificar_conceito


@pytest.mark.unit
@pytest.mark.parametrize(
    "media, conceito_esperado",
    [
        (6.0, "C"),
        (7.4, "C"),
        (7.5, "B"),
        (8.9, "B"),
        (9.0, "A"),
        (10.0, "A"),
    ],
    ids=[
        "bva_media_6_0_conceito_c",
        "bva_media_7_4_conceito_c",
        "bva_media_7_5_conceito_b",
        "bva_media_8_9_conceito_b",
        "bva_media_9_0_conceito_a",
        "bva_media_10_conceito_a",
    ],
)
def test_classificar_conceito_limites_para_aprovado(media: float, conceito_esperado: str) -> None:
    # Arrange
    situacao = Situacao.APROVADO

    # Act
    conceito = classificar_conceito(media, situacao)

    # Assert
    assert conceito == conceito_esperado


@pytest.mark.unit
@pytest.mark.parametrize(
    "media, conceito_esperado",
    [
        (7.45, "B"),
        (8.95, "A"),
        (5.95, "C"),
    ],
    ids=[
        "bva_media_7_45_arredonda_para_b",
        "bva_media_8_95_arredonda_para_a",
        "bva_media_5_95_arredonda_para_c",
    ],
)
def test_classificar_conceito_usa_media_arredondada(media: float, conceito_esperado: str) -> None:
    # Arrange
    situacao = Situacao.APROVADO

    # Act
    conceito = classificar_conceito(media, situacao)

    # Assert
    assert conceito == conceito_esperado


@pytest.mark.unit
@pytest.mark.parametrize(
    "media, situacao",
    [
        (5.0, Situacao.RECUPERACAO),
        (2.0, Situacao.REPROVADO_POR_NOTA),
        (9.5, Situacao.REPROVADO_POR_FALTA),
    ],
    ids=[
        "ep_recuperacao_conceito_d",
        "ep_reprovado_por_nota_conceito_d",
        "ep_reprovado_por_falta_com_nota_alta_conceito_d",
    ],
)
def test_classificar_conceito_nao_aprovado_recebe_d(media: float, situacao: Situacao) -> None:
    # Arrange
    entradas = (media, situacao)

    # Act
    conceito = classificar_conceito(*entradas)

    # Assert
    assert conceito == "D"


@pytest.mark.unit
@pytest.mark.parametrize(
    "media",
    [5.9, 0.0, 5.94],
    ids=[
        "eg_aprovado_com_media_5_9",
        "eg_aprovado_com_media_0",
        "eg_aprovado_com_media_5_94_que_arredonda_para_5_9",
    ],
)
def test_classificar_conceito_recusa_aprovado_com_media_baixa(media: float) -> None:
    # Arrange
    situacao = Situacao.APROVADO

    # Act
    with pytest.raises(ValueError) as erro:
        classificar_conceito(media, situacao)

    # Assert
    assert str(erro.value) == "Media incompativel com situacao APROVADO"


@pytest.mark.unit
@pytest.mark.parametrize(
    "media, situacao, erro_esperado, mensagem",
    [
        (8.0, "APROVADO", TypeError, "Situacao invalida"),
        (8.0, None, TypeError, "Situacao invalida"),
        ("8", Situacao.APROVADO, TypeError, "Media deve ser numerico"),
        (float("nan"), Situacao.APROVADO, ValueError, "Media deve ser um numero finito"),
        # Mesmo com conceito D garantido, uma média impossível precisa ser denunciada.
        (11, Situacao.REPROVADO_POR_FALTA, ValueError, "Media deve estar entre 0 e 10"),
    ],
    ids=[
        "eg_situacao_como_texto_e_nao_enum",
        "eg_situacao_none",
        "eg_media_como_texto",
        "eg_media_nan",
        "eg_media_invalida_nao_e_mascarada_pelo_conceito_d",
    ],
)
def test_classificar_conceito_recusa_entradas_invalidas(
    media: object, situacao: object, erro_esperado: type[Exception], mensagem: str
) -> None:
    # Arrange
    entradas = (media, situacao)

    # Act
    with pytest.raises(erro_esperado) as erro:
        classificar_conceito(*entradas)  # type: ignore[arg-type]

    # Assert
    assert str(erro.value) == mensagem
