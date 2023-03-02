# velib-paris

Sreaming et processing des dispo velib de PAris avec Kafka, PySpark et Databrick

Ce projet recupère les données des velib de Paris grâce à l'API, utilise Spark Streaming pour les traiter le flux et explore les données sur Databricks.

Requirements
Software

Pour run ce projet, les outils et leurs versions suivant sont nécessaire :

Kafka :https://kafka.apache.org/quickstart

Apache Spark: https://spark.apache.org/downloads.html

    Apache Kafka == 3.4.0
    Apache Spark == 3.2.3
    Python == 3.10
    Java == 11.0.18

## Python Libraries
Ce projet est entièrement érit en python. Pour utiliser l'ensemble du code nous avond besoin des bibliothéque suivante :

    Kafka-Python Python wrapper développé pour communicque avec Apache Kafka.

    pip install kafka-python

    requests Utiliser pour requeter l'API REST.

    pip install requests

Usage
Environment Setup

    Kafka: You will first of all need a working Kafka instance on your device. Follow the Kafka Quickstart section of the documentation to setup a single-node instance. You will need to create 3 distincts Kafka topics in order to run this project: Q1, Q2 and Q3. Run this command at the root of the Kafka folder to create the topic Q1:

    bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic Q1

    Spark: To use pyspark, you will need to install Spark on your device and note the installation path. This path is required by findspark to initialise PySpark at runtime:

    findspark.init('/opt/apache-spark')

    You will need to modify this path accordingly at the very beggining of actors/sparkConsumer.py.

Run projet
Pour lancer le projet, voici les commandes a utiliser dans des terminaux différents :
## Lancer Kafka

    $ bin/zookeeper-server-start.sh config/zookeeper.properties
    
    $ bin/kafka-server-start.sh config/server.properties
    
## Lancer le scipt pour la récupération et l'envoi 
    
    $python3 producer.py
  
 ## Lancer le scipt pour la récupération et la mise en csv
    
    $ python3 consumer.py
    
 ## Lancer le scipt pour le traitement en streaming des données
    
    $ $spark/bin/spark-submit \
    --master local --driver-memory 4g \
    --num-executors 2 --executor-memory 4g \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0 \
    ./streaming.py

Cette commande téléchargera la dépandance requise spark-sql-kafka-0-10_2.11:2.4.0 pour Spark. En fonction de votre version il est nécessaire d'ajuster cette commande

## Déatail des script
Le premier script permet de récupérer les données et de les envoyer via le producer kafka
Le second consumer récupère lles données et les agrége dans un fichier cvs
Le troisième permet de calculer en direct la dispibilitée de certain catégorie<\code>
  
