import time
import requests
import json
import pandas as pd
from kafka import KafkaProducer
from datetime import datetime


# Construire l'URL de l'API
api_url = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=velib-disponibilite-temps-reel%40montreuil&q=&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"
# api_url = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=velib-disponibilite-temps-reel@sevres-seineouest# &rows=10&start=0"

# Créer un producteur Kafka
producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

# Fonction pour récupérer les données d'une station
def get_velib_data(nrows):
    # Envoyer une requête GET à l'API
    response = requests.get(api_url)

    # Vérifier le statut de la réponse
    if response.status_code == 200:
        # Convertir les données de la réponse en un format JSON utilisable
        data = response.json()
        # Récupérer les données dans le champ "fields"
        fields = [record["fields"] for record in data["records"]]
        # Créer un dataframe à partir des données
        data = pd.DataFrame(fields)
        # Renvoyer les nrows premières lignes du dataframe
        return data.head(nrows)
    else:
        print("Erreur lors de la récupération des données")

# Fonction pour envoyer les données à Kafka
def send_data_to_kafka(data):
    # Convertir les données en format JSON
    json_data = json.dumps(data)
    producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    # Envoyer les données au topic "velib-data"
    producer.send("velib-data", json_data)
    producer.flush()
    print("Données envoyées à Kafka : ", datetime.now())

# Récupérer les données toutes les minutes
while True:
    data = get_velib_data(10)
    send_data_to_kafka(data.to_dict())
    time.sleep(60)