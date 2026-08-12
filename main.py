import os
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS
from loguru import logger
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "logs" / "app.log"

logger.add(LOG_FILE, encoding="utf-8")

DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
ORIGENS_PERMITIDAS = os.getenv("ORIGENS_PERMITIDAS", "*").split(",")

CORS(app, resources={
    r"/visualizado": {"origins": ORIGENS_PERMITIDAS},
    r"/logs": {"origins": ORIGENS_PERMITIDAS},
})

TAMANHO_MAXIMO = 20


def validar_campo(valor, nome_campo):
    if valor is None:
        return f"O parâmetro '{nome_campo}' é obrigatório."
    if not isinstance(valor, str) or valor == "":
        return f"O parâmetro '{nome_campo}' deve ser uma string não vazia."
    if len(valor) > TAMANHO_MAXIMO:
        return f"O parâmetro '{nome_campo}' deve ter no máximo {TAMANHO_MAXIMO} caracteres."
    if not valor.isalpha():
        return f"O parâmetro '{nome_campo}' deve conter apenas letras, sem números ou caracteres especiais."
    return None


@app.route('/visualizado', methods=['POST'])
def visualizado():
    nome = request.values.get('nome')
    texto = request.values.get('texto')

    erro = validar_campo(nome, 'nome') or validar_campo(texto, 'texto')
    if erro:
        logger.warning(f"Requisição inválida: {erro}")
        return jsonify({"erro": erro}), 400

    logger.info(f"Nome: {nome} | Texto {texto}")

    return jsonify({"mensagem": "Ok"}), 200


@app.route('/logs', methods=['GET'])
def ler_logs():
    if not LOG_FILE.exists():
        return jsonify({"logs": []}), 200

    linhas = LOG_FILE.read_text(encoding="utf-8").splitlines()

    return jsonify({"logs": linhas}), 200


if __name__ == '__main__':
    app.run(debug=DEBUG)
