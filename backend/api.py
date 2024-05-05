from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['gym_entry']
collection = db['entry']

@app.route('/api/entry', methods=['POST'])
def add_entry():
    data = request.get_json()
    member_id = data['member_id']
    entry_time = data['entry_time']
    session_duration = data['session_duration']

    # Ajouter une nouvelle entrée dans la base de données
    entry = {
        'member_id': member_id,
        'entry_time': entry_time,
        'session_duration': session_duration
    }
    collection.insert_one(entry)

    return jsonify({'message': 'Enregistrement ajouté avec succès !'}), 201

if __name__ == '__main__':
    app.run(debug=True)
