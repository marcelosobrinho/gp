from urllib.parse import quote_plus
from pymongo import MongoClient

# Substitua 'Triat!Sure@2024' pela sua senha real
password = 'Triat!Sure@2024'
encoded_password = quote_plus(password)

# Substitua '<password>' pela senha codificada
connection_string = f"mongodb+srv://triat:{encoded_password}@gp.8m9io.mongodb.net/?retryWrites=true&w=majority&appName=gp"

# Crie uma instância do cliente MongoDB
client = MongoClient(connection_string)
