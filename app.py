from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from datetime import datetime
from urllib.parse import quote_plus

# Criar a instância do Flask
app = Flask(__name__)
Bootstrap(app)

# Configuração do MongoDB na nuvem
password = 'Triat!Sure@2024'
encoded_password = quote_plus(password)
connection_string = f"mongodb+srv://triat:{encoded_password}@gp.8m9io.mongodb.net/?retryWrites=true&w=majority&appName=gp"
client = MongoClient(connection_string)
db = client['gp_database']
collection = db['registros']

# Definição das rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/controle-impressao', methods=['GET', 'POST'])
def controle_impressao():
    if request.method == 'POST':
        nome_cliente = request.form['nome_cliente']
        paginas_impressas = request.form['paginas_impressas']
        valor = request.form['valor']
        collection.insert_one({
            'nome_cliente': nome_cliente,
            'paginas_impressas': int(paginas_impressas),
            'valor': float(valor),
            'data_registro': datetime.now()
        })
        return redirect('/controle-impressao')

    clientes = collection.distinct('nome_cliente')
    return render_template('controle_impressao.html', clientes=clientes)

@app.route('/controle-certificado')
def controle_certificado():
    return "Página de Controle de Certificado (Em breve...)"

@app.route('/controle-teste1')
def controle_teste1():
    return "Página de Controle Teste1 (Em breve...)"

@app.route('/controle-teste2')
def controle_teste2():
    return "Página de Controle Teste2 (Em breve...)"

@app.route('/controle-teste3')
def controle_teste3():
    return "Página de Controle Teste3 (Em breve...)"

@app.route('/controle-teste4')
def controle_teste4():
    return "Página de Controle Teste4 (Em breve...)"

@app.route('/registros')
def registros():
    registros = collection.find()
    return render_template('registros.html', registros=registros)

if __name__ == '__main__':
    app.run(debug=True)
