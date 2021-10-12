from models import Pessoas, Usuarios

def insere_pessoa():
    pessoa = Pessoas(nome="Lua", idade=22)
    print(pessoa)
    pessoa.save()

def consulta_pessoas():
    pessoa = Pessoas.query.all()
    print(pessoa)

def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Gabriel')
    pessoa.delete()

def insere_usuario(login, senha):
    usuarios = Usuarios(login=login, senha=senha)
    usuarios.save()

def consulta_todos_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)

def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Gabriel').first()
    pessoa.idade = 23
    pessoa.save()

def insere_atividade():
    pessoa = Atividades(nome="Lua", idade=22)
    print(pessoa)
    pessoa.save()

def consulta_atividade():
    pessoa = Atividades.query.all()
    print(pessoa)

def exclui_atividade():
    pessoa = Atividades.query.filter_by(nome='Gabriel')
    pessoa.delete()

def altera_atividade():
    pessoa = Atividades.query.filter_by(nome='Gabriel').first()
    pessoa.idade = 23
    pessoa.save()

if __name__ == '__main__':
    #insere_pessoa()
    #altera_pessoa()
    #exclui_pessoa()
    #consulta_pessoas()
    insere_usuario('admin', 'admin')
