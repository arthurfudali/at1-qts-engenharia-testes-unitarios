"""RN03 a RN06 — Situação do aluno (PRD, seção 3).

Nos testes de limite as três notas são iguais, para que a média seja a própria nota.
"""

import pytest

from app.situacao_academica import Situacao, avaliar_situacao

FREQUENCIA_REGULAR = 90


@pytest.mark.unit
@pytest.mark.parametrize(
    "p1, p2, trabalho, frequencia, situacao_esperada",
    [
        (8.0, 7.0, 9.0, 90, Situacao.APROVADO),
        (5.0, 5.0, 5.0, 90, Situacao.RECUPERACAO),
        (2.0, 3.0, 1.0, 90, Situacao.REPROVADO_POR_NOTA),
        (8.0, 7.0, 9.0, 50, Situacao.REPROVADO_POR_FALTA),
    ],
    ids=[
        "ep_aprovado",
        "ep_recuperacao",
        "ep_reprovado_por_nota",
        "ep_reprovado_por_falta",
    ],
)
def test_avaliar_situacao_particoes(
    p1: float, p2: float, trabalho: float, frequencia: float, situacao_esperada: Situacao
) -> None:
    # Arrange
    entradas = (p1, p2, trabalho, frequencia)

    # Act
    situacao = avaliar_situacao(*entradas)

    # Assert
    assert situacao == situacao_esperada


@pytest.mark.unit
@pytest.mark.parametrize(
    "nota, situacao_esperada",
    [
        (3.9, Situacao.REPROVADO_POR_NOTA),
        (4.0, Situacao.RECUPERACAO),
        (5.9, Situacao.RECUPERACAO),
        (6.0, Situacao.APROVADO),
        (0.0, Situacao.REPROVADO_POR_NOTA),
        (10.0, Situacao.APROVADO),
    ],
    ids=[
        "bva_media_3_9_reprovado",
        "bva_media_4_0_recuperacao",
        "bva_media_5_9_recuperacao",
        "bva_media_6_0_aprovado",
        "bva_media_0_reprovado",
        "bva_media_10_aprovado",
    ],
)
def test_avaliar_situacao_limites_de_media(nota: float, situacao_esperada: Situacao) -> None:
    # Arrange
    p1 = p2 = trabalho = nota

    # Act
    situacao = avaliar_situacao(p1, p2, trabalho, FREQUENCIA_REGULAR)

    # Assert
    assert situacao == situacao_esperada


@pytest.mark.unit
@pytest.mark.parametrize(
    "frequencia, situacao_esperada",
    [
        (74.99, Situacao.REPROVADO_POR_FALTA),
        (75, Situacao.APROVADO),
        (75.01, Situacao.APROVADO),
        (0, Situacao.REPROVADO_POR_FALTA),
        (100, Situacao.APROVADO),
    ],
    ids=[
        "bva_frequencia_74_99_reprova",
        "bva_frequencia_75_avalia_nota",
        "bva_frequencia_75_01_avalia_nota",
        "bva_frequencia_0_reprova",
        "bva_frequencia_100_avalia_nota",
    ],
)
def test_avaliar_situacao_limites_de_frequencia(
    frequencia: float, situacao_esperada: Situacao
) -> None:
    # Arrange
    p1, p2, trabalho = 8.0, 8.0, 8.0

    # Act
    situacao = avaliar_situacao(p1, p2, trabalho, frequencia)

    # Assert
    assert situacao == situacao_esperada


@pytest.mark.unit
@pytest.mark.parametrize(
    "p1, p2, trabalho",
    [
        (10.0, 10.0, 10.0),
        (5.0, 5.0, 5.0),
        (1.0, 1.0, 1.0),
    ],
    ids=[
        "eg_falta_prevalece_sobre_nota_maxima",
        "eg_falta_prevalece_sobre_recuperacao",
        "eg_falta_prevalece_sobre_reprovacao_por_nota",
    ],
)
def test_avaliar_situacao_falta_prevalece_sobre_a_nota(
    p1: float, p2: float, trabalho: float
) -> None:
    # Arrange
    frequencia_insuficiente = 74.99

    # Act
    situacao = avaliar_situacao(p1, p2, trabalho, frequencia_insuficiente)

    # Assert
    assert situacao == Situacao.REPROVADO_POR_FALTA


@pytest.mark.unit
def test_avaliar_situacao_usa_media_arredondada() -> None:
    # Arrange
    # Média exata 5,95: arredonda para 6,0 e aprova (RN02). Com float + round() daria recuperação.
    p1, p2, trabalho = 5.8, 5.8, 6.3

    # Act
    situacao = avaliar_situacao(p1, p2, trabalho, FREQUENCIA_REGULAR)

    # Assert
    assert situacao == Situacao.APROVADO


@pytest.mark.unit
@pytest.mark.parametrize(
    "p1, p2, trabalho, frequencia, erro_esperado, mensagem",
    [
        (8.0, 8.0, 8.0, 101, ValueError, "Frequencia deve estar entre 0 e 100"),
        (8.0, 8.0, 8.0, None, TypeError, "Frequencia deve ser numerico"),
        (8.0, 8.0, 8.0, float("nan"), ValueError, "Frequencia deve ser um numero finito"),
        (12.0, 8.0, 8.0, 90, ValueError, "P1 deve estar entre 0 e 10"),
        (8.0, 8.0, "8", 90, TypeError, "Trabalho deve ser numerico"),
        # A frequência é ruim, mas a nota inválida precisa ser denunciada mesmo assim.
        (12.0, 8.0, 8.0, 10, ValueError, "P1 deve estar entre 0 e 10"),
    ],
    ids=[
        "eg_frequencia_acima_de_100",
        "eg_frequencia_none",
        "eg_frequencia_nan",
        "eg_nota_invalida",
        "eg_nota_como_texto",
        "eg_nota_invalida_nao_e_mascarada_pela_falta",
    ],
)
def test_avaliar_situacao_recusa_entradas_invalidas(
    p1: object,
    p2: object,
    trabalho: object,
    frequencia: object,
    erro_esperado: type[Exception],
    mensagem: str,
) -> None:
    # Arrange
    entradas = (p1, p2, trabalho, frequencia)

    # Act
    with pytest.raises(erro_esperado) as erro:
        avaliar_situacao(*entradas)  # type: ignore[arg-type]

    # Assert
    assert str(erro.value) == mensagem


@pytest.mark.unit
def test_situacao_e_comparavel_com_texto() -> None:
    # Arrange
    situacao = Situacao.REPROVADO_POR_FALTA

    # Act
    texto = str(situacao)

    # Assert
    assert texto == "REPROVADO_POR_FALTA"
