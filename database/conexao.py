import psycopg2
from psycopg2 import Error

def conectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="gestao_frotas",
            user="postgres",
            password="admin123",
            port="5432"
        )
        return conn
    except Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

if __name__ == "__main__":
    conexao = conectar()
    if conexao:
        print("✅ Conexão com o banco 'gestao_frotas' realizada com sucesso!")
        conexao.close()
