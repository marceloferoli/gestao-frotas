class Abastecimento:
    def __init__(self, veiculo_id: int, tipo_combustivel: str, litros: float, valor_total: float, km_abastecimento: int, id: int = None):
        if litros <= 0 or valor_total <= 0:
            raise ValueError("Litros e valor total devem ser maiores que zero.")
        self.id = id
        self.veiculo_id = veiculo_id
        self.tipo_combustivel = tipo_combustivel
        self.litros = litros
        self.valor_total = valor_total
        self.km_abastecimento = km_abastecimento

    @property
    def preco_por_litro(self) -> float:
        return round(self.valor_total / self.litros, 2)
