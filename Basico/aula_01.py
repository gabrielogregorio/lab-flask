from flask import Flask

app = Flask(__name__)

@app.route("/<int:id>")
def pessoas(id):
    return {"id":id, "nome":"Gregório", "Profissao":"Desenvolvedor"}

@app.route('/soma/<int:valor1>/<int:valor2>')
def soma(valor1, valor2):
    return {'soma':valor1+valor2}

if __name__ == "__main__":
    app.run(debug=True)
