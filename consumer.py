from kafka import KafkaConsumer
import csv
import json
import pandas as pd


# Construire un consumer Kafka
consumer = KafkaConsumer("velib-data", bootstrap_servers=["localhost:9092"])
# Fonction pour mettre sous format json
def format_json(dataframe):
    # Use json_normalize() to convert JSON to DataFrame
    dict = json.loads(dataframe)
    # Use pandas.DataFrame.from_dict() to Convert JSON to DataFrame
    df = pd.DataFrame.from_dict(dict)
    return df

# Boucle infinie pour récupérer les messages du topic Kafka
for msg in consumer:
    # Décoder le message et le convertir en dictionnaire Python
    data = json.loads(msg.value.decode())
    print(data)
   # Appel de fonction format_json
    df = format_json(data)
    # Enregistrer les données dans un fichier CSV
    df.to_csv('velib_data', sep='\t',mode='a', index=False, header=False)
