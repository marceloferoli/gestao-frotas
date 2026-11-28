import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()

def conectar():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

if __name__ == "__main__":
    conexao = conectar()
    if conexao:
        print("✅ Conexão segura via .env realizada com sucesso!")
        conexao.close()

