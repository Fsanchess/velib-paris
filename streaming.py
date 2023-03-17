#import findspark
#findspark.init('/home/bigdata/spark/python/lib')
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
import json



# Fonction pour calculer la moyenne pour chaque station disponible
def get_station_stats(rdd):
    # Convertir les données JSON en un dictionnaire Python
    data = json.loads(rdd[1])
    # Extraire les informations de chaque station
    for station in data:
        name = station["name"]
        mechanical = int(station["mechanical"])
        electrical = int(station["ebike"])
        free = int(station["numdocksavailable"])
        # Calculer la moyenne pour chaque type de vélo et le nombre de places libres
        avg_mechanical = mechanical / (mechanical + electrical) if (mechanical + electrical) > 0 else 0
        avg_electrical = electrical / (mechanical + electrical) if (mechanical + electrical) > 0 else 0
        avg_free = free
        # Afficher les résultats pour chaque station
        print("Station: {}, Mechanical bikes: {:.2f}, Electrical bikes: {:.2f}, Free slots: {:.2f}".format(name, avg_mechanical, avg_electrical, avg_free))
        # Stocker les résultats dans un fichier
        with open("station_stats.txt", "a") as f:
            f.write("Station: {}, Mechanical bikes: {:.2f}, Electrical bikes: {:.2f}, Free slots: {:.2f}\n".format(name, avg_mechanical, avg_electrical, avg_free))


if __name__ == "__main__":
    # Créer un contexte Spark Streaming avec un intervalle de traitement de 10 secondes
    spark = SparkSession.builder.appName("VelibStats").getOrCreate()
    # Définir les paramètres de connexion à Kafka
    kafka_params= "kafka:9092"
    #kafka_params = {"bootstrap.servers": "localhost:9092"}
    topics = "velib-data"

    # Créer un flux de données en temps réel à partir de Kafka
    kafka_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", kafka_params) \
    .option("subscribe", topics) \
    .option("startingOffsets", "earliest") \
    .load()\
    .selectExpr("CAST(value AS STRING)")

    #Requête streaming

    query = sdfRides.groupBy("mechanical").count()
    
    query.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start() \
    .awaitTermination()
    
    # Traiter le flux de données en temps réel pour calculer les statistiques de chaque station
    kafka_stream.foreachRDD(get_station_stats)

    # Démarrer le flux de données en temps réel
    kafka_stream.awaitTermination()