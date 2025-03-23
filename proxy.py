
from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_EMAIL = "4744060a5e00f1f98672"
API_KEY = "9f43d27a446caf695bc7"

@app.route("/api/pedidos")
def pedidos():
    mes = request.args.get("mes")
    if mes:
        url = f"https://api.awsli.com.br/v1/pedido/?data_criacao__gte={mes}-01&data_criacao__lte={mes}-31&limit=100"
    else:
        url = "https://api.awsli.com.br/v1/pedido/?limit=100"

    headers = {
        "Content-Type": "application/json",
        "X-API-EMAIL": API_EMAIL,
        "X-API-KEY": API_KEY
    }

    pedidos = []
    while url:
        r = requests.get(url, headers=headers)
        data = r.json()
        pedidos.extend(data.get("objects", []))
        url = data.get("meta", {}).get("next")

    produtos = {}
    for pedido in pedidos:
        for item in pedido.get("itens", []):
            nome = item["produto"]["nome"]
            qtd = item["quantidade"]
            preco = float(item["preco"])
            if nome not in produtos:
                produtos[nome] = {"nome": nome, "unidades": 0, "unitario": preco}
            produtos[nome]["unidades"] += qtd

    return jsonify(list(produtos.values()))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
