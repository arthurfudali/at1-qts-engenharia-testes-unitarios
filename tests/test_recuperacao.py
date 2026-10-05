"""RN07 — Resultado da recuperação: média final = (média + nota de recuperação) / 2 (PRD, seção 3)."""

from decimal import Decimal

import pytest

from app.situacao_academica import Situacao, avaliar_recuperacao, calcular_media_final


@pytest.mark.unit
@pytest.mark.parametrize(
    "media, nota_recuperacao, media_final_esperada",
    [
        (5.0, 7.0, Decimal("6.0")),
        (5.0, 6.8, Decimal("5.9")),
        (4.0, 7.9, Decimal("6.0")),
        (4.0, 7.8, Decimal("5.9")),
        (5.0, 0.0, Decimal("2.5")),
        (5.0, 10.0, Decimal("7.5")),
    ],
    ids=[
        "bva_media_final_6_0",
        "bva_media_final_5_9",
        "bva_media_final_5_95_arredonda_para_6_0",
        "bva_media_final_5_9_sem_arredondar_para_cima",
        "bva_recuperacao_nota_minima",
        "bva_recuperacao_nota_maxima",
    ],
)
def test_calcular_media_final(
    media: float, nota_recuperacao: float, media_final_esperada: Decimal
) -> None:
    # Arrange
    entradas = (media, nota_recuperacao)

    # Act
    media_final = calcular_media_final(*entradas)

    # Assert
    assert media_final == media_final_esperada


@pytest.mark.unit
@pytest.mark.parametrize(
    "media, nota_recuperacao, situacao_esperada",
    [
        (5.0, 7.0, Situacao.APROVADO),
        (5.0, 6.8, Situacao.REPROVADO_POR_NOTA),
        (4.0, 7.9, Situacao.APROVADO),
        (5.9, 10.0, Situacao.APROVADO),
        (4.0, 0.0, Situacao.REPROVADO_POR_NOTA),
    ],
    ids=[
        "bva_aprova_com_media_final_6_0",
        "bva_reprova_com_media_final_5_9",
        "bva_aprova_por_arredondamento",
        "ep_aprova_com_folga",
        "ep_reprova_com_folga",
    ],
)
def test_avaliar_recuperacao(
    media: float, nota_recuperacao: float, situacao_esperada: Situacao
) -> None:
    # Arrange
    entradas = (media, nota_recuperacao)

    # Act
    situacao = avaliar_recuperacao(*entradas)

    # Assert
    assert situacao == situacao_esperada


@pytest.mark.unit
@pytest.mark.parametrize(
    "media",
    [4.0, 5.9, 3.95],
    ids=[
        "bva_media_4_0_entra_na_recuperacao",
        "bva_media_5_9_entra_na_recuperacao",
        "bva_media_3_95_arredonda_para_4_0_e_entra",
    ],
)
def test_calcular_media_final_aceita_media_da_faixa_de_recuperacao(media: float) -> None:
    # Arrange
    nota_recuperacao = 8.0

    # Act
    media_final = calcular_media_final(media, nota_recuperacao)

    # Assert
    assert isinstance(media_final, Decimal)


@pytest.mark.unit
@pytest.mark.parametrize(
    "media",
    [3.9, 6.0, 5.95, 0.0, 10.0],
    ids=[
        "eg_media_3_9_ja_reprovado",
        "eg_media_6_0_ja_aprovado",
        "eg_media_5_95_arredonda_para_6_0_ja_aprovado",
        "eg_media_0",
        "eg_media_10",
    ],
)
def test_calcular_media_final_recusa_aluno_fora_da_recuperacao(media: float) -> None:
    # Arrange
    nota_recuperacao = 8.0

    # Act / Assert
    with pytest.raises(ValueError, match="Aluno nao esta em recuperacao"):
        calcular_media_final(media, nota_recuperacao)


@pytest.mark.unit
@pytest.mark.parametrize(
    "media, nota_recuperacao, erro_esperado, mensagem",
    [
        (5.0, 10.1, ValueError, "Nota de recuperacao deve estar entre 0 e 10"),
        (5.0, -0.1, ValueError, "Nota de recuperacao deve estar entre 0 e 10"),
        (5.0, None, TypeError, "Nota de recuperacao deve ser numerico"),
        (5.0, float("nan"), ValueError, "Nota de recuperacao deve ser um numero finito"),
        ("5", 8.0, TypeError, "Media deve ser numerico"),
        (11, 8.0, ValueError, "Media deve estar entre 0 e 10"),
        (True, 8.0, TypeError, "Media deve ser numerico"),
    ],
    ids=[
        "eg_recuperacao_acima_de_10",
        "eg_recuperacao_negativa",
        "eg_recuperacao_none",
        "eg_recuperacao_nan",
        "eg_media_como_texto",
        "eg_media_acima_de_10",
        "eg_media_bool",
    ],
)
def test_avaliar_recuperacao_recusa_entradas_invalidas(
    media: object, nota_recuperacao: object, erro_esperado: type[Exception], mensagem: str
) -> None:
    # Arrange
    entradas = (media, nota_recuperacao)

    # Act / Assert
    with pytest.raises(erro_esperado, match=mensagem):
        avaliar_recuperacao(*entradas)  # type: ignore[arg-type]


@pytest.mark.unit
def test_avaliar_recuperacao_aceita_media_vinda_de_calcular_media() -> None:
    # Arrange
    # A média chega como Decimal quando vem de calcular_media; o fluxo inteiro precisa funcionar.
    media = Decimal("5.0")
    nota_recuperacao = Decimal("7.0")

    # Act
    situacao = avaliar_recuperacao(media, nota_recuperacao)

    # Assert
    assert situacao == Situacao.APROVADO
