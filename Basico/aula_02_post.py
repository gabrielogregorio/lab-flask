from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route('/soma', methods=["POST", "GET"])
def soma():
    dic_estrutura = {"sucesso":False, "msg_erro":"", "soma":""}

    if request.method == "POST":
        dados = json.loads( request.data )
        dic_estrutura["soma"] = sum(dados['valores'])
        dic_estrutura["sucesso"] = True

    elif request.method == "GET":
        dic_estrutura["soma"] = 0
        dic_estrutura["msg_erro"] = "Você precisa informar os valores com o método POST"
        dic_estrutura["sucesso"] = False

    return jsonify(dic_estrutura)


if __name__ == "__main__":
    app.run(debug=True)
