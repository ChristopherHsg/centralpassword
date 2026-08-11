from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from .db import inicializar_banco
from .db import conectar
from datetime import datetime

load_dotenv()

app = Flask(__name__, template_folder="../templates")


# ==========================================
# PÁGINA INICIAL
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# TOTEM
# ==========================================

@app.route("/totem")
def totem():
    return render_template("totem.html")


# ==========================================
# GUICHÊ
# ==========================================

@app.route("/guiche/<int:id>")
def guiche(id):
    return render_template("guiche.html", guiche=id)


# ==========================================
# INICIALIZAR BANCO
# ==========================================

@app.cli.command("init-db")
def init_db():
    inicializar_banco()
    print("Banco de dados inicializado!")


# ==========================================
# GERAR NOVA SENHA
# ==========================================

@app.route("/nova/<tipo>")
def nova_senha(tipo):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT MAX(numero)
        FROM senha
        WHERE tipo = ?
    """, (tipo,))

    ultimo = cursor.fetchone()[0]

    if ultimo is None:
        ultimo = 0

    numero = ultimo + 1

    cursor.execute("""
        INSERT INTO senha
        (tipo, numero, status, horario)
        VALUES (?, ?, ?, ?)
    """, (
        tipo,
        numero,
        "aguardando",
        datetime.now()
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "senha": f"{tipo}{numero:03d}"
    })


# ==========================================
# CHAMAR PRÓXIMA SENHA
# ==========================================

@app.route("/proxima/<int:guiche>")
def proxima_senha(guiche):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM senha
        WHERE status = 'aguardando'
        ORDER BY id
        LIMIT 1
    """)

    senha = cursor.fetchone()

    if senha is None:

        conn.close()

        return jsonify({
            "erro": "Sem senhas"
        })

    cursor.execute("""
        UPDATE senha
        SET status = 'atendendo',
            guiche = ?
        WHERE id = ?
    """, (
        guiche,
        senha["id"]
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "senha": f"{senha['tipo']}{senha['numero']:03d}",
        "guiche": guiche
    })


# ==========================================
# ÚLTIMA SENHA ATENDENDO
# ==========================================

@app.route("/ultima_senha")
def ultima_senha():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM senha
        WHERE status = 'atendendo'
        ORDER BY id DESC
        LIMIT 1
    """)

    senha = cursor.fetchone()

    conn.close()

    if senha is None:
        return jsonify({
            "senha": "---",
            "guiche": "---"
        })

    return jsonify({
        "senha": f"{senha['tipo']}{senha['numero']:03d}",
        "guiche": senha["guiche"]
    })


# ==========================================
# EXECUTAR SERVIDOR
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)