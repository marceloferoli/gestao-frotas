class Veiculo:
    def __init__(self, placa: str, modelo: str, ano: int, km_atual: int = 0, status: str = "Ativo", id: int = None):
        self.id = id
        self.placa = placa.upper().strip()
        self.modelo = modelo.strip()
        self.ano = ano
        self.km_atual = km_atual
        self.status = status

    def atualizar_km(self, novo_km: int):
        if novo_km < self.km_atual:
            raise ValueError(f"Erro: A nova quilometragem ({novo_km}) não pode ser menor que a atual ({self.km_atual}).")
        self.km_atual = novo_km

    def __str__(self):
        return f"[{self.placa}] {self.modelo} ({self.ano}) - {self.km_atual} km | Status: {self.status}"
