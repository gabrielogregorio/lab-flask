from flask import Flask, jsonify, request
import json

app = Flask(__name__)

desenvolvedores = [
    {'nome':'Sara Jacob',
    'habilidades':['Python','Ruby']
    },
    {'nome':'Daniela Martins',
    'habilidades':['Python','Django']
    },
    {'nome':'Julia Maria dos Santos',
    'habilidades':['Python','Flask']
    }
]


@app.route("/dev/<int:id>/", methods=["GET", "PUT", "DELETE"])
def desenvolvedor(id):
    if request.method == "GET":
        try:
            resposta = desenvolvedores[id]
        except IndexError:
            resposta = {'status':'erro', 'mensagem':'Id do desenvolvedor {} não existe'.format(id)}

        return jsonify(resposta)

    elif request.method == "PUT":
        dados = json.loads( request.data )
        desenvolvedores[id] = dados
        return jsonify(dados)

    elif request.method == "DELETE":
        desenvolvedores.pop(id)
        return jsonify({"status":"sucesso","mensagem":"Registro Excuido"})


@app.route("/dev", methods=["POST", "GET"])
def lista_devs():
    if request.method== "POST":
        dados = json.loads(request.data)
        posicao = len(desenvolvedores)
        desenvolvedores.append(dados)
        return jsonify({"status":'sucesso','mensagem':'Registro Inserido na posicao {}!'.format(posicao-1)})

    elif request.method == "GET":
        return jsonify(desenvolvedores)


if __name__ == "__main__":
    app.run(debug=True)
