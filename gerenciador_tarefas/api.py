from flask import Flask, jsonify, request, render_template, make_response
from json import loads, JSONDecodeError
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

tarefas = {}

PERMITIDAS = ['tarefa','responsável', 'status']


def valida_dados_entradas(entrada_dict):
    """
        Retorna True se o dicionário
        seguir um template especifico
    """

    if entrada_dict != {}:
        # Lista todas as chaves do dicionário
        lista_chaves = list(entrada_dict.keys())

        # Verifica se tem o mesmo número de chaves
        if len(lista_chaves) != len(PERMITIDAS):
            return [False, "Erro, Existem chaves a mais ou a menos do que o permito!"]

        # Loop por todas a chaves
        for chave in lista_chaves:
            # Verifica se a chave não está permitida
            if chave not in PERMITIDAS:
                return [False, "Valor de chave não permitido!"]

        return [True, ""]

    return [False, "Erro, o dicionário está vazio"]


def carregar_json(txt_json):
    # Se não for informado um json
    if txt_json == b'':
        return [False, {"sucesso":False, "mensagem":"Você precisa informar o Json"}]

    # Tente carregar o json
    try:
        entrada_dict = loads( txt_json )
    except JSONDecodeError:
        return [False, {"sucesso":False, "mensagem":"Json invalido!"}]

    # Valida o json
    valor_valido = valida_dados_entradas(entrada_dict)

    # Se não for válido
    if not valor_valido[0]:
        return [False, {"sucesso":False, "mensagem":valor_valido[1]}]

    return [True, entrada_dict ]


def obter_proximo_id():
    proximo_id = 1
    if tarefas != {}:
       proximo_id = max(tarefas.keys()) + 1

    return proximo_id


class Apresentacao(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)


class Tarefas(Resource):   
    def get(self, id):
        try:
            return jsonify(tarefas[id])
        except KeyError:
            return jsonify({"status":"erro", "mensagem":"Id não existe!"})

    def put(self, id):
        json = carregar_json(request.data)
        if not json[0]:
            return jsonify( json[1] )

        if id in tarefas:
            tarefas[ id ] = dict(json[1])
            return jsonify( tarefas[ id ] )

        return jsonify({"sucesso":False, "mensagem":"Id {} nao está registrado!".format(id)})

    def delete(self, id):
        if id in tarefas:
            del tarefas[ id ]
            return jsonify({"sucesso":False, "mensagem":"Item {} removido!".format(id)})

        return jsonify({"sucesso":False, "mensagem":"Id {} nao está registrado!".format(id)})


class InsereTarefa(Resource):
   def post(self):
        json = carregar_json(request.data)

        if not json[0]:
            return jsonify( json[1] )

        id = obter_proximo_id()
        tarefas[ id ] = dict(json[1])

        return jsonify({"sucesso":True, "mensagem":"Valor Inserido com sucesso na posicao {}".format(id)})


class ListaTarefas(Resource):
    def get(self):
        return jsonify(tarefas)

api.add_resource(Apresentacao, "/")
api.add_resource(ListaTarefas, "/task")
api.add_resource(Tarefas, "/task/<int:id>")
api.add_resource(InsereTarefa, "/add")


if __name__ == "__main__":
    app.run(debug=True)
