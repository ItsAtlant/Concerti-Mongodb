from bson import ObjectId
from pymongo import MongoClient

url = "mongodb+srv://ItsAtlant:irRNEj7rfzvzpWw7.@cluster0.gbqxuqm.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)

print(client)
mydb = client["ConcertoDB"]
mycollection = mydb["Biglietti_venduti"]

mydict = \
    {
        "id_concerto": ObjectId("648c38abab40123ad77944d2"),
        "prezzo_pagato": 40,
        "Anello/locazione": "prima fila",
        "Nome e Cognome": "Davide Soltys",
        "data acquisto": "22/04/2023"
    }

mycollection.insert_one(mydict)
#collegamento