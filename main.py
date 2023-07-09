from bson import ObjectId
from pymongo import MongoClient
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from functools import partial
import datetime
import dotenv
import os
import json

JSON_PATH = "vat.json"

def city_to_contry(city):
    geocode_en = partial(geolocator.geocode, language="en")
    location = geocode_en(city)
    return location.address.split(", ")[-1]

def print_ticket(x):
    print("Nome concerto:", collection_concerti.find_one(ObjectId(x["id concerto"]))["Nome"])
    print(f"Prezzo: {x['prezzo pagato']}€")
    fix_data = str(x['data acquisto']).split(".")[0]
    print(f"Data acquisto: {fix_data} \n")

def print_concert(x):
    print(f"\n{x['Nome']} ", end="")
    if type(x["data"]) == list:
        for dataConcert in x["data"]:
            fix_data = str(dataConcert).split(".")[0]
            print(f" - {fix_data}", end="")
        print("\n", end="")
    else:
        print(x["data"])
    print(f"({x['_id']})")
    print(f"Città: {x['locazione']}")
    print("Artista: ", end="")
    for artista in x["artisti"]:
        print(artista, end=" ")
    print(f"\nCapacità: {x['capacità']}\n")

# Initialize Nominatim API
geolocator = Nominatim(user_agent="MyApp")
# connect with mongo

dotenv.load_dotenv()
client = MongoClient(os.environ["MONGO_CONNECTION"])
mydb = client["ConcertoDB"]
collection_biglietti = mydb["Biglietti_venduti"]
collection_concerti = mydb["Concerto"]

# login
nickname = input("Ciao benvenuto nell'app dei concerti, perfavore inserisci il tuo nick name: ")

# scelta
while True:
    try:
        scelta = int(input("0. Visualizzazione dei tuoi biglietti digitare\n1. Acquistare un biglietto\n2. EXIT\nScegli: "))
    except ValueError:
        print("Input non valido, riprova")
        continue
    # visualizzare i biglietti
    match scelta:
        case 0:
            my_query = {"nome utente": nickname}
            project = {"nome concerto": 1, "id concerto": 1, "data concerto": 1, "prezzo pagato": 1, "data acquisto": 1}

            for i, x in enumerate(collection_biglietti.find(my_query, project).sort("data concerto", 1)):
                print_ticket(x)
                if i == 4:
                    break

        case 1:
            data = datetime.datetime.now()
            formatted_date = {"$date": data}
            myquery = {"data": {"$gte": data}}
            project = {"coordinate": 0}

            for i, x in enumerate(collection_concerti.find(myquery, project).sort("data", 1)):
                print_concert(x)
                if i == 4:
                    break
            print("Digitare R per cercare l'artista")
            print("Digitare V per cercare per vicinanza")
            print("Digitare S per cercare per costo")
            print("Digitare N per cercare per nome del concerto")
            print("Digitare Q per acquistare")
            print("Digitare ESC per tornare nel menù\n")

            scelta = input("inserire la propria scelta: ")
            match scelta:
                case "Q":
                    try:
                        with open(JSON_PATH, "r") as f:
                            VAT_RATES = json.load(f)
                    except:
                        print("Errore durante l'apertura del file")
                        break

                    citta = input("Inserisci la citta dove abiti: ")
                    paese = city_to_contry(citta)
                    location = geolocator.geocode(citta)
                    get_iva = VAT_RATES[paese]
                    print("l'iva nel tuo paese è del ", get_iva, "%")
                    id_concerto = input("Inserisci l'ID del concerto per cui desideri acquistare i biglietti: ")
                    disponibilita = collection_biglietti.count_documents({"id concerto": ObjectId(id_concerto)})
                    numero_di_posti_liberi = collection_concerti.find_one({"_id": ObjectId(id_concerto)}, {"capacità": 1})["capacità"]-disponibilita
                    print("Sono rimasti",numero_di_posti_liberi, "biglietti disponibili")
                    num_biglietti = int(input("Inserisci il numero di biglietti che desideri acquistare: "))

                    # Verifica disponibilità dei biglietti
                    if disponibilita + num_biglietti <= \
                            collection_concerti.find_one({"_id": ObjectId(id_concerto)}, {"capacità": 1})["capacità"]:
                        costo = collection_concerti.find_one({"_id": ObjectId(id_concerto)}, {"costo no iva": 1})[
                            "costo no iva"]
                        for _ in range(num_biglietti):
                            data_acquisto = datetime.datetime.now()

                            # Creazione del documento per l'acquisto
                            documento_acquisto = {
                                "nome utente": nickname,
                                "id concerto": ObjectId(id_concerto),
                                "prezzo pagato": (costo + costo * get_iva / 100),
                                "data acquisto": data_acquisto
                            }

                            # Inserimento del documento nella collezione "Biglietti_venduti"
                            result = collection_biglietti.insert_one(documento_acquisto)

                            if result.inserted_id:
                                print("Acquisto completato con successo!")
                            else:
                                print("Si è verificato un errore durante l'acquisto.")
                    else:
                        print("Il numero richiesto di biglietti non è disponibile per il concerto selezionato.")
                
                case "R":
                    artista = input("Inserisci il nome del artista desiderato: ")

                    myquery = {
                        "data": {"$gte": data},
                        "artisti": artista
                    }
                    project = {"coordinate": 0}

                    for x in collection_concerti.find(myquery, project).sort("data", 1):
                        print_concert(x)

                case "N":
                    nome = input("Inserisci il nome del concerto desiderato: ")

                    myquery = {
                        "data": {"$gte": data},
                        "Nome": nome
                    }
                    project = {"coordinate": 0}

                    for x in collection_concerti.find(myquery, project).sort("data", 1):
                        print_concert(x)       
                
                case "S":
                    costo_max = float(input("Inserisci il costo massimo desiderato: "))

                    myquery = {
                        "data": {"$gte": data},
                        "costo no iva": {"$lte": costo_max}
                    }
                    project = {"coordinate": 0}

                    for x in collection_concerti.find(myquery, project).sort("data", 1):
                        print_concert(x)
                
                case "V":
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

                        print_concert(x)
                        print("Distanza: {:.2f} km".format(concert_distance))
                        print("\n")

                case "ESC":
                    break
               
                case default:
                    print("Input non valido")
                    continue
        
        case 2:
            break

        case default:
            print("Input non valido")
            continue