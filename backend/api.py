from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes de l'application

# Connexion à la base de données MongoDB
client = MongoClient('localhost', 27017)
db = client['gym_entry']
collection = db['entry']


# Endpoint pour enregistrer une entrée
@app.route('/api/entry', methods=['POST'])
def add_entry():
    data = request.json
    if 'member_id' not in data:
        return jsonify({'error': 'Missing member_id'}), 400
    entry = {
        'member_id': data['member_id'],
        'entry_time': datetime.now()
    }
    result = collection.insert_one(entry)
    return jsonify({'message': 'Entry added successfully', 'entry_id': str(result.inserted_id)}), 201


# Endpoint pour récupérer toutes les entrées
@app.route('/api/entries', methods=['GET'])
def get_entries():
    entries = list(collection.find({}, {'_id': 0}))  # Exclure l'ID MongoDB
    return jsonify(entries), 200


if __name__ == '__main__':
    app.run(debug=True)
