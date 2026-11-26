from models.manutencao import Manutencao
from services.frota_service import FrotaService

revisao = Manutencao(
    veiculo_id=1,
    tipo="Preventiva",
    descricao="Troca de óleo do motor, filtros de diesel e inspeção de freios",
    custo=1850.00,
    km_manutencao=145800
)

FrotaService.registrar_manutencao(revisao, novo_status="Ativo")
FrotaService.relatorio_custos_veiculo(1)
