from bson import ObjectId
from bson import DatetimeConversion
from pymongo import MongoClient
from functools import partial   
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import datetime
from bson import ObjectId
from bson import DatetimeConversion
from pymongo import MongoClient
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import datetime
import requests
import pycountry
from pycountry_convert import country_alpha2_to_country_name
from functools import partial


VAT_RATES = {
    "Afghanistan": 0,
    "Albania": 20,
    "Algeria": 19,
    "Andorra": 4.5,
    "Angola": 14,
    "Antigua and Barbuda": 15,
    "Argentina": 21,
    "Armenia": 20,
    "Australia": 10,
    "Austria": 20,
    "Azerbaijan": 18,
    "Bahamas": 0,
    "Bahrain": 5,
    "Bangladesh": 15,
    "Barbados": 17.5,
    "Belarus": 20,
    "Belgium": 21,
    "Belize": 12.5,
    "Benin": 18,
    "Bhutan": 7,
    "Bolivia": 13,
    "Bosnia and Herzegovina": 17,
    "Botswana": 12,
    "Brazil": 0,
    "Brunei": 0,
    "Bulgaria": 20,
    "Burkina Faso": 18,
    "Burundi": 18,
    "Cambodia": 10,
    "Cameroon": 19.25,
    "Canada": 5,
    "Cape Verde": 15,
    "Central African Republic": 19.6,
    "Chad": 18,
    "Chile": 19,
    "China": 13,
    "Colombia": 19,
    "Comoros": 15,
    "Congo (Brazzaville)": 18,
    "Congo (Kinshasa)": 16,
    "Costa Rica": 13,
    "Croatia": 25,
    "Cuba": 0,
    "Cyprus": 19,
    "Czech Republic": 21,
    "Denmark": 25,
    "Djibouti": 7,
    "Dominica": 15,
    "Dominican Republic": 18,
    "Ecuador": 12,
    "Egypt": 14,
    "El Salvador": 13,
    "Equatorial Guinea": 18,
    "Eritrea": 15,
    "Estonia": 20,
    "Eswatini": 15,
    "Ethiopia": 15,
    "Fiji": 9,
    "Finland": 24,
    "France": 20,
    "Gabon": 18,
    "Gambia": 15,
    "Georgia": 18,
    "Germany": 19,
    "Ghana": 12.5,
    "Greece": 24,
    "Grenada": 15,
    "Guatemala": 12,
    "Guinea": 18,
    "Guinea-Bissau": 18,
    "Guyana": 14,
    "Haiti": 10,
    "Honduras": 15,
    "Hungary": 27,
    "Iceland": 24,
    "India": 18,
    "Indonesia": 10,
    "Iran": 9,
    "Iraq": 10,
    "Ireland": 23,
    "Israel": 17,
    "Italy": 22,
    "Jamaica": 15,
    "Japan": 10,
    "Jordan": 16,
    "Kazakhstan": 12,
    "Kenya": 16,
    "Kiribati": 12,
    "Kosovo": 18,
    "Kuwait": 0,
    "Kyrgyzstan": 12,
    "Laos": 10,
    "Latvia": 21,
    "Lebanon": 11,
    "Lesotho": 15,
    "Liberia": 10,
    "Libya": 9,
    "Liechtenstein": 7.7,
    "Lithuania": 21,
    "Luxembourg": 17,
    "Madagascar": 20,
    "Malawi": 16.5,
    "Malaysia": 6,
    "Maldives": 6,
    "Mali": 18,
    "Malta": 18,
    "Marshall Islands": 0,
    "Mauritania": 20,
    "Mauritius": 15,
    "Mexico": 16,
    "Micronesia": 0,
    "Moldova": 20,
    "Monaco": 20,
    "Mongolia": 10,
    "Montenegro": 19,
    "Morocco": 20,
    "Mozambique": 17,
    "Myanmar (Burma)": 5,
    "Namibia": 15,
    "Nauru": 0,
    "Nepal": 13,
    "Netherlands": 21,
    "New Zealand": 15,
    "Nicaragua": 15,
    "Niger": 19,
    "Nigeria": 7.5,
    "North Korea": 10,
    "North Macedonia": 18,
    "Norway": 25,
    "Oman": 5,
    "Pakistan": 17,
    "Palau": 0,
    "Panama": 7,
    "Papua New Guinea": 10,
    "Paraguay": 10,
    "Peru": 18,
    "Philippines": 12,
    "Poland": 23,
    "Portugal": 23,
    "Qatar": 0,
    "Romania": 19,
    "Russia": 20,
    "Rwanda": 18,
    "Saint Kitts and Nevis": 17,
    "Saint Lucia": 12,
    "Saint Vincent and the Grenadines": 16,
    "Samoa": 15,
    "San Marino": 10,
    "Sao Tome and Principe": 15,
    "Saudi Arabia": 15,
    "Senegal": 18,
    "Serbia": 20,
    "Seychelles": 15,
    "Sierra Leone": 15,
    "Singapore": 7,
    "Slovakia": 20,
    "Slovenia": 22,
    "Solomon Islands": 0,
    "Somalia": 0,
    "South Africa": 15,
    "South Korea": 10,
    "South Sudan": 0,
    "Spain": 21,
    "Sri Lanka": 8,
    "Sudan": 0,
    "Suriname": 10,
    "Sweden": 25,
    "Switzerland": 7.7,
    "Syria": 10,
    "Taiwan": 5,
    "Tajikistan": 18,
    "Tanzania": 18,
    "Thailand": 7,
    "Timor-Leste": 0,
    "Togo": 18,
    "Tonga": 0,
    "Trinidad and Tobago": 12.5,
    "Tunisia": 19,
    "Turkey": 18,
    "Turkmenistan": 15,
    "Tuvalu": 0,
    "Uganda": 18,
    "Ukraine": 20,
    "United Arab Emirates": 5,
    "United Kingdom": 20,
    "United States": 0,
    "Uruguay": 22,
    "Uzbekistan": 15,
    "Vanuatu": 0,
    "Vatican City": 0,
    "Venezuela": 16,
    "Vietnam": 10,
    "Yemen": 5,
    "Zambia": 16,
    "Zimbabwe": 0
}
def city_to_contry(city):
    geocode_en = partial(geolocator.geocode, language="en")
    location = geocode_en(city)
    return location.address.split(", ")[-1]

def print_ticket(x):
    print(f"ID concerto: {x['_id']}")
    print(f"Prezzo: {x['prezzo pagato']}€")
    fix_data = str(x['data acquisto']).split(".")[0]
    print(f"Data acquisto: {fix_data}")

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
            print_ticket(x)


    if scelta == 1:
        data = datetime.datetime.now()
        formatted_date = {"$date": data}
        myquery = {"data": {"$gte": data}}
        project = {"coordinate": 0}

        for x in collection_concerti.find(myquery,project).sort("data", 1):
            print_concert(x)


        print("Digitare R per cercare l'artista")
        print("Digitare V per cercare per vicinanza") # fatto
        print("Digitare S per cercare per costo")
        print("Digitare N per cercare per nome del concerto")
        print("Digitare Q per acquistare")
        print("Digitare ESC per tornare nel menù")
        scelta = input("inserire la propria scelta: ")
        if scelta == "Q":

            citta = input("Inserisci la citta dove abiti: ")
            paese = city_to_contry(citta)
            location = geolocator.geocode(citta)
            get_iva = VAT_RATES[paese]
            print(get_iva)
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
        if scelta == "R":
            artista = input("Inserisci il nome del artista desiderato: ")

            myquery = {
                "data": {"$gte": data},
                "artisti": artista
            }
            project = {"coordinate": 0}

            for x in collection_concerti.find(myquery, project).sort("data", 1):
                print_concert(x)

        
        if scelta == "N":
            nome = input("Inserisci il nome del concerto desiderato: ")

            myquery = {
                "data": {"$gte": data},
                "Nome": nome
            }
            project = {"coordinate": 0}

            for x in collection_concerti.find(myquery, project).sort("data", 1):
                print_concert(x)
        
        
        if scelta == "S":
            costo_max = float(input("Inserisci il costo massimo desiderato: "))

            myquery = {
                "data": {"$gte": data},
                "costo no iva": {"$lte": costo_max}
            }
            project = {"coordinate": 0}

            for x in collection_concerti.find(myquery, project).sort("data", 1):
                print_concert(x)


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

                print_concert(x)
                print("Distanza: {:.2f} km".format(concert_distance))
                print("\n")
