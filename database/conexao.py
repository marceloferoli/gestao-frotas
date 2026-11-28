import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
from services.logger import logger

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
        logger.info("Conexão com o PostgreSQL estabelecida com sucesso.")
        return conn
    except Error as e:
        logger.error(f"Falha crítica ao conectar no PostgreSQL: {e}")
        return None

if __name__ == "__main__":
    conexao = conectar()
    if conexao:
        conexao.close()
