import sqlite3
import os


def conectar():
    caminho = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "instance",
            "database.db"
        )
    )

    print(f"Usando banco: {caminho}")

    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row

    return conn


def inicializar_banco():
    conn = conectar()

    caminho_schema = os.path.join(
        os.path.dirname(__file__),
        "schema.sql"
    )

    with open(caminho_schema, "r", encoding="utf-8") as arquivo:
        conn.executescript(arquivo.read())

    conn.commit()
    conn.close()