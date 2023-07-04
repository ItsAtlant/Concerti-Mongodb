from cryptography.fernet import Fernet
import datetime
from header import *

def acquista():
    return

def descrizione():
    return

def cerca():
    return

  
def main():
    client, db = init_database()
    collection = get_collection(db, collection_name = "Concerti")

    user = False
    while not user:

        print("\nWelcome to <name of service>!")
        print("1. Login\n2. Registrazione")
        choice = int(input())

        if choice == 1:
            user = login(db)
            print(user)
        elif choice == 2:
            user = register(db)
            print(user)
        else:
            raise ValueError("Valore non valido")

    while True:
        print("Visualizazione 5 concerti più recenti:")
        visualizza_concerti(db)
        while True:
            try:
                scelta = int(input("1) Acquista\n2) Descrizione\n3) Cerca\n4) Esci\n"))
            except ValueError:
                print("Inserisci un numero da 1 a 4")
            else:
                break

        if scelta == 1:
            # TODO funzione acquista
            print("Acquista")
        elif scelta == 2:
            # TODO funzione descrizione
            print("Descrizione")
        elif scelta == 3:
            # TODO funzione cerca
            print("Cerca")
        elif scelta == 4:
            client.close()
            print("Arrivederci!")
            break

if __name__ == "__main__":
    main()