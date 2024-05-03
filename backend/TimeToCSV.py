import csv
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('localhost', 27017)
db = client['gym_entry']
collection = db['entry']

# Récupérer toutes les entrées de la base de données
entries = list(collection.find({}, {'_id': 0, 'member_id': 1, 'entry_time': 1}))

# Créer un fichier CSV et écrire les entrées
with open('entries.csv', 'w', newline='') as csvfile:
    fieldnames = ['Nom', 'Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for entry in entries:
        writer.writerow({'Nom': entry['member_id'], 'Date': entry['entry_time']})
