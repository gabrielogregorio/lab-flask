from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)


@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False

    #return USUARIOS.get(login) == senha
    return Usuarios.query.filter_by(login=login, senha=senha).first()


class Pessoa(Resource):

    @auth.login_required
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        print(pessoa)

        if pessoa is not None:
            response = {
                'nome':pessoa.nome,
                'idade':pessoa.idade,
                'id':pessoa.id
            }

        else:
            response = {
                'status':'erro',
                'mensagem': 'Pessoa não cadastrada'
            }

        return response

    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json

        if 'nome' in dados.keys():
            pessoa.nome = dados['nome']

        if 'idade' in dados.keys():
            pessoa.idade = dados['idade']
        pessoa.save()

        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response

    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        mensagem = 'Pessoa {} escluida com sucesso'.format(pessoa.nome)
        pessoa.delete()

        return {'status':'sucesso', 'mensagem':mensagem}


class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        
        return [{'id':x.id, 'nome':x.nome, 'idade':x.idade} for x in pessoas]

    def post(self):
        dados = request.json
        pessoa = Pessoas(
            idade=dados['idade'],
            nome=dados['nome'],
            id=dados['id']
        )
        pessoa.save()

        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response

class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()

        response = []
        for i in atividades:
            id = i.id
            nome = i.nome
            pessoa = i.pessoa
            pessoa_nome = pessoa.nome if pessoa is not None else ""
            status = i.status

            response.append({'id':id, 'nome':nome, 'pessoa':pessoa_nome, 'status':status})

        return response
    
    # Adicioar atividade
    def post(self):
        """
            # http://127.0.0.1:5000
            # cadastra uma nova
            # /atividades/
            # {'pessoa':atividade.pessoa.nome,'nome':atividade.nome, 'id':atividade.id}
        """
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        if pessoa is None: return {"status":"Pessoa não cadastrada"}

        atividade = Atividades(nome=dados['nome'], pessoa=pessoa, status=dados['status'])


        atividade.save()

        response = {
            'pessoa':atividade.pessoa.nome,
            'nome':atividade.nome,
            'id':atividade.id,
            'status':atividade.status
        }

        return response

class ListaAtividadesPorPessoa(Resource):
    def get(self, nome):
        """
            # http://127.0.0.1:5000
            # Lista todas as atividades de uma pessoa
            # /pessoa/atividade/nome_pessoa
        """
        pessoa = Pessoas.query.filter_by(nome=nome).first()

        if pessoa is not None:
            atividades = Atividades.query.filter_by(pessoa_id = pessoa.id)

            if atividades is not None:
                return [{'id':a.id, 'atividade':a.nome, 'pessoa':pessoa.nome, 'status':a.status} for a in atividades]

            return {}
        return {'status':'erro', 'mensagem':'Usuário "{}" não cadastrado'.format(nome)}


class AlterarStatusAtividade(Resource):
    def put(self, id, status):
        """
            # http://127.0.0.1:5000
            # ALtera o status de uma atividade
            # /atividades/id_atividade/novo_status

        """
        atividades = Atividades.query.filter_by(id=id).first()

        if atividades is not None:
            atividades.status = status
            atividades.save()

            response = {
                'id':atividades.id,
                'atividade':atividades.nome,
                'status':atividades.status
            }

            return response


        return {'status':'erro', 'mensagem':'Id {} não cadastrado'.format(id)}


api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas,'/pessoa/')
api.add_resource(ListaAtividades,'/atividades/')
api.add_resource(ListaAtividadesPorPessoa, '/pessoa/atividade/<string:nome>')
api.add_resource(AlterarStatusAtividade, '/atividades/<int:id>/<string:status>')

if __name__ == '__main__':
    app.run(debug=True)
