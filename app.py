from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient
import urllib.parse
from bson.objectid import ObjectId

app = Flask(__name__)

# Codificar a senha corretamente
username = "triat"
password = urllib.parse.quote_plus("Triat!Sure@2024")
cluster = "gp.8m9io.mongodb.net"
db_name = "gp_database"

# URI de conexão
client = MongoClient(f'mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=gp')
db = client[db_name]

# Coleções
setor_collection = db['setores']  # Nome da coleção de setores
cliente_collection = db['clientes']  # Nome da coleção de clientes
impressora_collection = db['impressoras']  # Nome da coleção de impressoras
controle_impressao_collection = db['controle_impressao']  # Nome da coleção de Controle de Impressora
controle_almoxarifado_collection = db['controle_almoxarifado']  # Coleção para o controle de almoxarifado

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cliente/novo', methods=['GET', 'POST'])
def novo_cliente():
    if request.method == 'POST':
        nome_cliente = request.form['nome']
        
        # Inserir o novo cliente no banco de dados
        cliente_collection.insert_one({"nome_cliente": nome_cliente})
        
        return redirect('/')  # Redirecionar para a página inicial após o cadastro

    return render_template('cliente_novo.html')

@app.route('/cliente/listar')
def listar_clientes():
    clientes = cliente_collection.find()
    return render_template('listar_clientes.html', clientes=clientes)

@app.route('/cliente/alterar/<cliente_id>', methods=['GET', 'POST'])
def alterar_cliente(cliente_id):
    cliente = cliente_collection.find_one({"_id": ObjectId(cliente_id)})
    
    if request.method == 'POST':
        nome_cliente = request.form['nome']
        
        # Atualizar o nome do cliente
        cliente_collection.update_one(
            {"_id": ObjectId(cliente_id)},
            {"$set": {"nome_cliente": nome_cliente}}
        )
        
        return redirect('/cliente/listar')

    return render_template('alterar_cliente.html', cliente=cliente)

@app.route('/setor/novo', methods=['GET', 'POST'])
def setor_novo():
    if request.method == 'POST':
        nome_setor = request.form['nome']
        
        # Inserir apenas o nome_setor no banco de dados
        setor_collection.insert_one({
            'nome_setor': nome_setor
        })

        return redirect('/')  # Redirecionar para a página inicial após o cadastro

    return render_template('setor_novo.html')

@app.route('/setor/listar')
def listar_setores():
    setores = setor_collection.find()
    return render_template('listar_setores.html', setores=setores)

@app.route('/setor/alterar/<setor_id>', methods=['GET', 'POST'])
def alterar_setor(setor_id):
    setor = setor_collection.find_one({"_id": ObjectId(setor_id)})
    
    if request.method == 'POST':
        nome_setor = request.form['nome']
        
        # Atualizar o nome do setor
        setor_collection.update_one(
            {"_id": ObjectId(setor_id)},
            {"$set": {"nome_setor": nome_setor}}
        )
        
        return redirect('/setor/listar')

    return render_template('alterar_setor.html', setor=setor)

@app.route('/impressora/novo', methods=['GET', 'POST'])
def impressora_novo():
    setores = setor_collection.find()
    if request.method == 'POST':
        nome_impressora = request.form['nome']
        setor_id = request.form['setor']
        tipo_impressora = request.form['tipo']

        impressora_collection.insert_one({
            'nome': nome_impressora,
            'setor': ObjectId(setor_id),
            'tipo': tipo_impressora
        })

        return redirect('/impressora/listar')

    return render_template('novo_impressora.html', setores=setores)

@app.route('/impressora/listar')
def listar_impressoras():
    impressoras = impressora_collection.find()
    setores = {setor['_id']: setor['nome_setor'] for setor in setor_collection.find()}  # Dicionário para mapear setor_id a nome_setor
    return render_template('listar_impressoras.html', impressoras=impressoras, setores=setores)

@app.route('/impressora/alterar/<impressora_id>', methods=['GET', 'POST'])
def alterar_impressora(impressora_id):
    setores = setor_collection.find()
    impressora = impressora_collection.find_one({"_id": ObjectId(impressora_id)})

    if request.method == 'POST':
        nome_impressora = request.form['nome']
        setor_id = request.form['setor']
        tipo_impressora = request.form['tipo']

        impressora_collection.update_one(
            {"_id": ObjectId(impressora_id)},
            {"$set": {
                "nome": nome_impressora,
                "setor": ObjectId(setor_id),
                "tipo": tipo_impressora
            }}
        )

        return redirect('/impressora/listar')

    return render_template('alterar_impressora.html', impressora=impressora, setores=setores)

@app.route('/controle_impressao/novo', methods=['GET', 'POST'])
def novo_controle_impressao():
    if request.method == 'POST':
        impressora_id = request.form['impressora']
        cliente_id = request.form['cliente']
        data_impressao = request.form['data_impressao']
        quantidade = int(request.form['quantidade'])

        # Inserir o controle de impressão no banco de dados
        controle_impressao_collection.insert_one({
            'impressora_id': ObjectId(impressora_id),
            'cliente_id': ObjectId(cliente_id),
            'data_impressao': data_impressao,
            'quantidade': quantidade
        })

        return redirect('/controle_impressao/listar')

    impressoras = impressora_collection.find()
    clientes = cliente_collection.find()
    return render_template('controle_impressao_novo.html', impressoras=impressoras, clientes=clientes)

@app.route('/controle_impressao/listar')
def listar_controle_impressao():
    registros = controle_impressao_collection.find()
    impressoras = {impressora['_id']: impressora['nome'] for impressora in impressora_collection.find()}
    clientes = {cliente['_id']: cliente['nome_cliente'] for cliente in cliente_collection.find()}
    return render_template('listar_controle_impressao.html', registros=registros, impressoras=impressoras, clientes=clientes)

@app.route('/controle_impressao/alterar/<registro_id>', methods=['GET', 'POST'])
def alterar_controle_impressao(registro_id):
    registro = controle_impressao_collection.find_one({"_id": ObjectId(registro_id)})
    
    if request.method == 'POST':
        impressora_id = request.form['impressora']
        cliente_id = request.form['cliente']
        data_impressao = request.form['data_impressao']
        quantidade = int(request.form['quantidade'])
        
        # Atualizar o registro de controle de impressão
        controle_impressao_collection.update_one(
            {"_id": ObjectId(registro_id)},
            {"$set": {
                'impressora_id': ObjectId(impressora_id),
                'cliente_id': ObjectId(cliente_id),
                'data_impressao': data_impressao,
                'quantidade': quantidade
            }}
        )
        
        return redirect('/controle_impressao/listar')

    impressoras = impressora_collection.find()
    clientes = cliente_collection.find()
    return render_template('alterar_controle_impressao.html', registro=registro, impressoras=impressoras, clientes=clientes)

@app.route('/controle_impressao/pesquisar', methods=['GET'])
def pesquisar_controle_impressao():
    termo = request.args.get('termo', '')
    campo = request.args.get('campo', 'impressora_nome')  # Campo selecionado pelo usuário

    # Inicializar a lista de resultados
    resultado = []

    if campo == 'impressora_nome':
        impressoras = impressora_collection.find({"nome": {"$regex": termo, "$options": "i"}})
        impressora_ids = [impressora['_id'] for impressora in impressoras]

        registros = controle_impressao_collection.find({"impressora_id": {"$in": impressora_ids}})

        for registro in registros:
            impressora = impressora_collection.find_one({"_id": registro['impressora_id']})
            cliente = cliente_collection.find_one({"_id": registro['cliente_id']})
            resultado.append({
                'impressora_nome': impressora['nome'],
                'cliente_nome': cliente['nome_cliente'],
                'data_impressao': registro['data_impressao'],
                'quantidade': registro['quantidade'],
                'id': str(registro['_id'])
            })

    elif campo == 'cliente_nome':
        clientes = cliente_collection.find({"nome_cliente": {"$regex": termo, "$options": "i"}})
        cliente_ids = [cliente['_id'] for cliente in clientes]

        registros = controle_impressao_collection.find({"cliente_id": {"$in": cliente_ids}})

        for registro in registros:
            impressora = impressora_collection.find_one({"_id": registro['impressora_id']})
            cliente = cliente_collection.find_one({"_id": registro['cliente_id']})
            resultado.append({
                'impressora_nome': impressora['nome'],
                'cliente_nome': cliente['nome_cliente'],
                'data_impressao': registro['data_impressao'],
                'quantidade': registro['quantidade'],
                'id': str(registro['_id'])
            })

    elif campo == 'data_impressao':
        registros = controle_impressao_collection.find({"data_impressao": {"$regex": termo}})

        for registro in registros:
            impressora = impressora_collection.find_one({"_id": registro['impressora_id']})
            cliente = cliente_collection.find_one({"_id": registro['cliente_id']})
            resultado.append({
                'impressora_nome': impressora['nome'],
                'cliente_nome': cliente['nome_cliente'],
                'data_impressao': registro['data_impressao'],
                'quantidade': registro['quantidade'],
                'id': str(registro['_id'])
            })

    return jsonify(resultado)

@app.route('/almoxarifado/novo', methods=['GET', 'POST'])
def novo_almoxarifado():
    if request.method == 'POST':
        impressora_id = request.form['impressora']
        data_resma = request.form['data_resma']
        quantidade_resma = int(request.form['quantidade_resma'])

        # Inserir o controle de almoxarifado no banco de dados
        controle_almoxarifado_collection.insert_one({
            'impressora_id': ObjectId(impressora_id),
            'data_resma': data_resma,
            'quantidade_resma': quantidade_resma
        })

        return redirect('/almoxarifado/listar')

    impressoras = impressora_collection.find()
    return render_template('almoxarifado_novo.html', impressoras=impressoras)

@app.route('/almoxarifado/listar')
def listar_almoxarifado():
    registros = controle_almoxarifado_collection.find()
    impressoras = {impressora['_id']: impressora['nome'] for impressora in impressora_collection.find()}
    return render_template('listar_almoxarifado.html', registros=registros, impressoras=impressoras)

@app.route('/almoxarifado/alterar/<registro_id>', methods=['GET', 'POST'])
def alterar_almoxarifado(registro_id):
    registro = controle_almoxarifado_collection.find_one({"_id": ObjectId(registro_id)})
    
    if request.method == 'POST':
        impressora_id = request.form['impressora']
        data_resma = request.form['data_resma']
        quantidade_resma = int(request.form['quantidade_resma'])

        # Atualizar o registro de controle de almoxarifado
        controle_almoxarifado_collection.update_one(
            {"_id": ObjectId(registro_id)},
            {"$set": {
                'impressora_id': ObjectId(impressora_id),
                'data_resma': data_resma,
                'quantidade_resma': quantidade_resma
            }}
        )
        
        return redirect('/almoxarifado/listar')

    impressoras = impressora_collection.find()
    return render_template('alterar_almoxarifado.html', registro=registro, impressoras=impressoras)

@app.template_filter('nome_impressora')
def nome_impressora_filter(impressora_id):
    impressora = impressora_collection.find_one({"_id": ObjectId(impressora_id)})
    return impressora['nome'] if impressora else 'Desconhecido'

@app.template_filter('nome_cliente')
def nome_cliente_filter(cliente_id):
    cliente = cliente_collection.find_one({"_id": ObjectId(cliente_id)})
    return cliente['nome_cliente'] if cliente else 'Desconhecido'

if __name__ == '__main__':
    app.run(debug=True)
