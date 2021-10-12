import json
from flask import Flask, request
from flask_restful import Resource, Api
from skils import Habilidades, listaHabilidades, alteraHabilidades

app = Flask(__name__)
api = Api(app)

devs = [
    {
        "id":0,
        "nome":"Gabriel",
        "skils":["Python", "Java"]
    },
    {
        "id":1,
        "nome":"Julia",
        "skils":["C#", "Java"]
    }
]


class Desenvolvedor(Resource):
    def get(self, id):
        try:
            resposta = devs[id]
        except IndexError:
            resposta = {'status':'erro', 'mensagem':'Id do desenvolvedor {} não existe'.format(id)}

        return resposta

    def put(self, id):
        dados = json.loads( request.data )
        devs[id] = dados
        return dados

    def delete(self, id):
        devs.pop(id)
        return {"status":"sucesso","mensagem":"Registro Excuido"}

    def post(self):
        return {"metodo":"post"}

class ListaDevs(Resource):
    def get(self):
        return devs

    def post(self):
        dados = dict(json.loads(request.data))
        posicao = len(devs)
        devs.append(dados)

        return {"status":'sucesso','mensagem':'Registro Inserido na posicao {}!'.format(posicao-1)}


api.add_resource(Desenvolvedor, '/dev/<int:id>')
api.add_resource(ListaDevs, '/dev/')
api.add_resource(listaHabilidades, '/skils/')
api.add_resource(Habilidades, '/skils/<string:skill>')
api.add_resource(alteraHabilidades, '/skils/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
