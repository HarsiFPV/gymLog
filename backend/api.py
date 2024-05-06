from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

app = Flask(__name__)
CORS(app)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.gym_entry
users_collection = db.users
entries_collection = db.entries

# Route pour ajouter une nouvelle entrée
@app.route('/api/entry', methods=['POST'])
def add_entry():
    data = request.get_json()
    user_id = data['user_id']
    entry_time = data['entry_time']
    session_duration = data['session_duration']

    # Ajouter une nouvelle entrée dans la base de données
    entry = {
        'user_id': user_id,
        'entry_time': entry_time,
        'session_duration': session_duration
    }
    entries_collection.insert_one(entry)

    return jsonify({'message': 'Enregistrement ajouté avec succès !'}), 201


@app.route('/api/users', methods=['GET'])
def get_users():
    # Récupérer tous les utilisateurs de la base de données
    users = list(users_collection.find({}, {'_id': 1, 'first_name': 1, 'last_name': 1}))

    # Convertir les identifiants d'utilisateur en chaînes de caractères
    for user in users:
        user['_id'] = str(user['_id'])

        # Supprimer la clé 'last_name' si elle est vide
        if not user['last_name']:
            del user['last_name']

    return jsonify(users)


# Route pour ajouter un nouvel utilisateur
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    # Enregistrement de l'utilisateur dans la base de données et récupération de son ID
    user_id = users_collection.insert_one({'first_name': first_name, 'last_name': last_name}).inserted_id

    # Conversion de l'ID de l'utilisateur en une chaîne de caractères
    user_id_str = str(user_id)

    # Création de l'objet utilisateur à renvoyer dans la réponse JSON
    user = {'_id': user_id_str, 'first_name': first_name}

    # Ajouter le nom de famille s'il est disponible
    if last_name:
        user['last_name'] = last_name

    # Renvoi de la réponse JSON avec l'objet utilisateur
    return jsonify(user), 201

if __name__ == '__main__':
    app.run(debug=True)
