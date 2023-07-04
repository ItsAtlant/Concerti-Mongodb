# Base
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from datetime import datetime
# Password handling
from cryptography.fernet import Fernet
from getpass import getpass
# Output formatting
from rich import print
from rich.console import Console
from rich.table import Table
# Key Management System
from kms import kms
# Environment Variables
import dotenv
from dotenv import dotenv_values

config = {
    **dotenv_values(".env.mongodb"),  # load mongodb variables
    **os.environ,  # override loaded values with environment variables
}

# Fernet Encr. Key -------------------------
fernet = kms()

# Connessione al DB
def init_database(db_name="TicketMaster"):
    dotenv.load_dotenv()
    CONNECTION_STRING = dotenv_values(".env.mongodb").get("MONGO_CONNECTION_STRING")

    # Create a new client and connect to the server
    uri = CONNECTION_STRING 
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return client, client[db_name]
    # ritorna il db e la connessione

# Get a collection
def get_collection(db, collection_name="Concerti"):
    return db[collection_name]

# Registrazione nuovo utente
def register(db):
    
    user = input("Inserisci username: ")
    email = input("Inserisci email: ")
    password = getpass("Inserisci password: ").encode()

    # User data
    user_data = {"Username": user, "Email": email, "Password": fernet.encrypt(password)}

    # Switch to Users collection
    users_coll = get_collection(db, collection_name = "Users")
    # Check on collection
    if users_coll.count_documents({}) == 0:
        print(users_coll)
    

    # Check if user already registered
    try:
        while users_coll.find_one({"Username": user}) is not None:
            print("Username già registrato. Scegline uno diverso: ")
            user = input()
    except:
        # può dare errore se la collection users non esiste ancora
        # mongodb crea le collection solo al momento del primo insert
        print("Users collection does not exist yet")
        pass

    # Insert new user
    users_coll.insert_one(user_data)
    print(f"Benvenuto, {user}!")

    return user

# Login
def login(db):
    email = input("Inserisci email: ")
    password = getpass("Inserisci password: ").encode()

    # Switch to Users collection
    users_coll = get_collection(db, collection_name = "Users")
    # Check if user is registered
    stored_userData = {}
    try:
        stored_userData = users_coll.find_one({"Email": email})
    except:
        #client.close()
        raise ValueError("Errore nella ricerca")
    
    if stored_userData is None:
        print("Utente non registrato")
        return True
    else:
        # Get stored username & password
        #stored_userData = users_coll.find({"Email": email})
        stored_username = stored_userData.get("Username")
        #print("password", stored_userData.get("Password").decode())
        stored_pass = fernet.decrypt( stored_userData.get("Password").decode() )

        if stored_pass != password:
            raise ValueError("Password errata")
        print(f"Benvenuto, {stored_username}!")
    return stored_username

# Visualizza i 5 concerti prossimi
def visualizza_concerti(db):
    # Switch to Concerti collection
    concerti_coll = get_collection(db, collection_name="Concerti")

    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Find the next 5 concerts after the current date
    next_concerts = concerti_coll.find({"Data": {"$gte": current_date}}).sort("Data", 1).limit(5)

    console = Console()

    # Create a table
    table = Table(show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("Nome")
    table.add_column("Location")
    table.add_column("Artisti")
    table.add_column("Date")
    table.add_column("Sezioni")

    for concert in next_concerts:
        nome = concert["Nome"]
        location = f"{concert['Location']['Nome Locale']}, {concert['Location']['Indirizzo']}, {concert['Location']['Città']}, {concert['Location']['Provincia']}, {concert['Location']['Regione']}"
        artisti = "\n".join(concert["Artisti"])
        date = "\n".join(concert["Data"])

        sezioni = []
        for sezione in concert["Sezioni"]:
            sezioni.append(f"{sezione['Nome']}\nPosti Disponibili: {sezione['Posti Disponibili']}\nCosto: {sezione['Costo']}")
        sezioni = "\n\n".join(sezioni)

        table.add_row(nome, location, artisti, date, sezioni)
        table.add_row("")

    console.print(table)