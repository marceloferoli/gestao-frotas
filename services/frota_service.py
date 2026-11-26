from database.conexao import conectar
from models.veiculo import Veiculo
from models.abastecimento import Abastecimento
from models.manutencao import Manutencao

class FrotaService:
    @staticmethod
    def cadastrar_veiculo(veiculo: Veiculo):
        conn = conectar()
        if not conn:
            return False, "Erro de conexão com o banco de dados."
        try:
            with conn.cursor() as cur:
                sql = """
                    INSERT INTO veiculos (placa, modelo, ano, km_atual, status)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id;
                """
                cur.execute(sql, (veiculo.placa, veiculo.modelo, veiculo.ano, veiculo.km_atual, veiculo.status))
                veiculo.id = cur.fetchone()[0]
                conn.commit()
                return True, f"Veículo {veiculo.placa} ({veiculo.modelo}) cadastrado com sucesso!"
        except Exception as e:
            conn.rollback()
            return False, "Erro ao cadastrar veículo: verifique se a placa já existe."
        finally:
            conn.close()

    @staticmethod
    def registrar_abastecimento(abastecimento: Abastecimento):
        conn = conectar()
        if not conn:
            return False, "Erro de conexão com o banco de dados."
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT placa, km_atual FROM veiculos WHERE id = %s;", (abastecimento.veiculo_id,))
                resultado = cur.fetchone()
                if not resultado:
                    return False, "Veículo não encontrado."

                placa, km_anterior = resultado
                if abastecimento.km_abastecimento <= km_anterior:
                    return False, f"Bloqueado: o KM informado ({abastecimento.km_abastecimento}) deve ser maior que o odômetro atual ({km_anterior} km)."

                km_rodados = abastecimento.km_abastecimento - km_anterior
                media_kml = round(km_rodados / abastecimento.litros, 2)

                cur.execute("""
                    INSERT INTO abastecimentos (veiculo_id, tipo_combustivel, litros, valor_total, km_abastecimento)
                    VALUES (%s, %s, %s, %s, %s);
                """, (abastecimento.veiculo_id, abastecimento.tipo_combustivel, abastecimento.litros, abastecimento.valor_total, abastecimento.km_abastecimento))

                cur.execute("UPDATE veiculos SET km_atual = %s WHERE id = %s;", (abastecimento.km_abastecimento, abastecimento.veiculo_id))

                conn.commit()
                return True, f"Abastecimento ({abastecimento.tipo_combustivel}) registrado [{placa}] — R$ {abastecimento.preco_por_litro}/L | Média nesse trecho: {media_kml} km/l."
        except Exception as e:
            conn.rollback()
            return False, f"Erro ao registrar abastecimento: {e}"
        finally:
            conn.close()

    @staticmethod
    def registrar_manutencao(manutencao: Manutencao, novo_status: str = "Ativo"):
        conn = conectar()
        if not conn:
            return False, "Erro de conexão com o banco de dados."
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT placa, km_atual FROM veiculos WHERE id = %s;", (manutencao.veiculo_id,))
                resultado = cur.fetchone()
                if not resultado:
                    return False, "Veículo não encontrado."

                placa, km_atual = resultado
                if manutencao.km_manutencao < km_atual:
                    return False, f"Bloqueado: o KM da manutenção ({manutencao.km_manutencao}) não pode ser menor que o atual ({km_atual} km)."

                cur.execute("""
                    INSERT INTO manutencoes (veiculo_id, tipo, descricao, custo, km_manutencao)
                    VALUES (%s, %s, %s, %s, %s);
                """, (manutencao.veiculo_id, manutencao.tipo, manutencao.descricao, manutencao.custo, manutencao.km_manutencao))

                cur.execute("""
                    UPDATE veiculos SET km_atual = %s, status = %s WHERE id = %s;
                """, (manutencao.km_manutencao, novo_status, manutencao.veiculo_id))

                conn.commit()
                return True, f"Manutenção ({manutencao.tipo}) registrada para [{placa}] | Status atualizado: {novo_status}."
        except Exception as e:
            conn.rollback()
            return False, f"Erro ao registrar manutenção: {e}"
        finally:
            conn.close()

    @staticmethod
    def obter_dados_dashboard():
        conn = conectar()
        if not conn:
            return [], {"combustivel": 0, "manutencao": 0, "total": 0}
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        v.id, v.placa, v.modelo, v.ano, v.km_atual, v.status,
                        COALESCE((SELECT SUM(valor_total) FROM abastecimentos WHERE veiculo_id = v.id), 0) AS comb,
                        COALESCE((SELECT SUM(custo) FROM manutencoes WHERE veiculo_id = v.id), 0) AS manut,
                        COALESCE((SELECT SUM(litros) FROM abastecimentos WHERE veiculo_id = v.id), 0) AS total_litros,
                        (SELECT MIN(km_abastecimento) FROM abastecimentos WHERE veiculo_id = v.id) AS primeiro_km,
                        (SELECT MAX(km_abastecimento) FROM abastecimentos WHERE veiculo_id = v.id) AS ultimo_km
                    FROM veiculos v
                    ORDER BY v.id;
                """)
                linhas = cur.fetchall()
                veiculos = []
                total_comb = 0
                total_manut = 0
                for l in linhas:
                    comb = float(l[6])
                    manut = float(l[7])
                    litros = float(l[8])
                    p_km = l[9]
                    u_km = l[10]

                    if litros > 0 and p_km and u_km and u_km > p_km:
                        media_kml = f"{round((u_km - p_km) / litros, 2)} km/l"
                    elif litros > 0:
                        media_kml = "1º abastec."
                    else:
                        media_kml = "—"

                    total_comb += comb
                    total_manut += manut
                    veiculos.append({
                        "id": l[0], "placa": l[1], "modelo": l[2],
                        "ano": l[3], "km_atual": l[4], "status": l[5],
                        "combustivel": comb, "manutencao": manut,
                        "total": comb + manut, "media_kml": media_kml
                    })
                resumo = {
                    "combustivel": total_comb,
                    "manutencao": total_manut,
                    "total": total_comb + total_manut
                }
                return veiculos, resumo
        finally:
            conn.close()
