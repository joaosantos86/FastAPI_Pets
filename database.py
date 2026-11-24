import os
from contextlib import closing
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))


def ler_configuracao():
    return {
        "host": os.environ["DB_HOST"],
        "port": int(os.environ["DB_PORT"]),
        "database": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
    }


def criar_conexao():
    return mysql.connector.connect(**ler_configuracao())


def executar_sql(sql, parametros=()):
    with closing(criar_conexao()) as conexao:
        with closing(conexao.cursor(dictionary=True)) as cursor:
            cursor.execute(sql, parametros)
            return cursor.fetchall()
