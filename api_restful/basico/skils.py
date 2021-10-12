import json
from flask_restful import Resource, request

habilidades = ['Python', 'Java', 'Flask', 'PHP']


class listaHabilidades(Resource):
	def get(self):
		return habilidades


class Habilidades(Resource):
	def post(self, skill):
		if skill not in habilidades:
			habilidades.append(skill)
			return habilidades

		return {"Erro":"Habilidade já cadastrada"}


class alteraHabilidades(Resource):
	def put(self, id):
		if id < 0 or id > len(habilidades)-1:
			return {"Erro":"Indice não existe!"}

		dados = dict(json.loads(request.data))
		habilidades[id] = dados["nome"]

		return habilidades

	def delete(self, id):
		if id < 0 or id > len(habilidades)-1:
			return {"Erro":"Indice não existe!"}

		del habilidades[id]
		return habilidades
