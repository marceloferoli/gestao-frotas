class Manutencao:
    def __init__(self, veiculo_id: int, tipo: str, descricao: str, custo: float, km_manutencao: int, id: int = None):
        self.id = id
        self.veiculo_id = veiculo_id
        self.tipo = tipo  # 'Preventiva' ou 'Corretiva'
        self.descricao = descricao
        self.custo = custo
        self.km_manutencao = km_manutencao
