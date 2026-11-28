from unittest.mock import MagicMock, patch
from services.frota_service import FrotaService
from models.abastecimento import Abastecimento
from models.manutencao import Manutencao

@patch("services.frota_service.conectar")
def test_bloqueia_abastecimento_com_km_menor_ou_igual(mock_conectar):
    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    mock_cursor.fetchone.return_value = ("ABC-1D23", 10000)
    mock_conectar.return_value = mock_conn

    abastecimento_invalido = Abastecimento(
        veiculo_id=1,
        tipo_combustivel="Gasolina Aditivada",
        litros=40.0,
        valor_total=240.0,
        km_abastecimento=9500
    )

    sucesso, mensagem = FrotaService.registrar_abastecimento(abastecimento_invalido)

    assert sucesso is False
    assert "Bloqueado" in mensagem

@patch("services.frota_service.conectar")
def test_registra_abastecimento_valido_e_calcula_kml(mock_conectar):
    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    mock_cursor.fetchone.return_value = ("ABC-1D23", 10000)
    mock_conectar.return_value = mock_conn

    abastecimento_valido = Abastecimento(
        veiculo_id=1,
        tipo_combustivel="Diesel S10",
        litros=50.0,
        valor_total=300.0,
        km_abastecimento=10500
    )

    sucesso, mensagem = FrotaService.registrar_abastecimento(abastecimento_valido)

    assert sucesso is True
    assert "10.0 km/l" in mensagem
    mock_conn.commit.assert_called_once()

@patch("services.frota_service.conectar")
def test_bloqueia_manutencao_com_km_retroativo(mock_conectar):
    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    mock_cursor.fetchone.return_value = ("ABC-1D23", 10500)
    mock_conectar.return_value = mock_conn

    manutencao_invalida = Manutencao(
        veiculo_id=1,
        tipo="Preventiva",
        descricao="Troca de óleo",
        custo=450.0,
        km_manutencao=10200
    )

    sucesso, mensagem = FrotaService.registrar_manutencao(manutencao_invalida)

    assert sucesso is False
    assert "Bloqueado" in mensagem
