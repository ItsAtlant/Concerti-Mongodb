from bson import ObjectId
from bson import DatetimeConversion
from pymongo import MongoClient
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import datetime


# Initialize Nominatim API
geolocator = Nominatim(user_agent="MyApp")

# connect with mongo
url = "mongodb+srv://ItsAtlant:irRNEj7rfzvzpWw7.@cluster0.gbqxuqm.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)
mydb = client["ConcertoDB"]
collection_biglietti = mydb["Biglietti_venduti"]
collection_concerti = mydb["Concerto"]

# login
nickname = input("Ciao benvenuto nell'app dei concerti, perfavore inserisci il tuo nick name: ")

# scelta
while True:
    scelta = int(input("Per acquistare un biglietto premere 1, se vuoi visualizzare i tuoi biglietti premi 0: "))
    # visualizzare i biglietti
    if scelta == 0:
        my_query = {"nome utente": nickname}
        project = {"nome concerto": 1, "data concerto": 1, "prezzo pagato": 1, "data acquisto": 1}

        for x in collection_biglietti.find(my_query, project).sort("data concerto", 1):
            print(x, "\n")

    if scelta == 1:
        data = datetime.datetime.now()
        formatted_date = {"$date": data}

        myquery = {"data": {"$gte": data}}
        project = {"coordinate": 0}

        for x in collection_concerti.find(myquery, project).sort("data", 1):
            print(x, "\n")

        print("Digitare R per cercare l'artista")
        print("Digitare V per cercare per vicinanza") # fatto
        print("Digitare S per cercare per costo")
        print("Digitare N per cercare per nome")
        print("Digitare A per cercare per artista")
        print("Digitare Q per acquistare")
        print("Digitare ESC per tornare nel menù")
        scelta = input("inserire la propria scelta: ")

        if scelta == "V":
            citta = input("Inserisci la citta dove abiti: ")
            location = geolocator.geocode(citta)
            collection_concerti.create_index([("coordinate", "2dsphere")])
            distance_range = input("Inserisci entro quanti km: ")
            myquery = {
                "data": {"$gte": data},
                "coordinate": {
                    "$near": {
                        "$geometry": {
                            "type": "Point",
                            "coordinates": [location.longitude, location.latitude]
                        },
                        "$maxDistance": int(distance_range) * 1000
                    }
                }
            }
            project = {}

            for x in collection_concerti.find(myquery, project).sort("coordinate", 1):
                concert_coordinates = x["coordinate"]["coordinates"]
                reference_coordinates = [location.longitude, location.latitude]
                concert_distance = geodesic((reference_coordinates[1], reference_coordinates[0]), (concert_coordinates[1], concert_coordinates[0])).kilometers

                print(x)
                print("Distanza: {:.2f} km".format(concert_distance))
                print("\n")
