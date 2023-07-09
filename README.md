 # 🎶Concert-Ticket🎫 MongoDB

## Descrizione 🚀

Il Programma Biglietti Concerto è un'applicazione Python che consente agli utenti di cercare e acquistare biglietti per concerti. L'applicazione utilizza il database MongoDB per archiviare informazioni sui concerti e i biglietti venduti.

## Librerie Python Utilizzate 🚩

Il programma utilizza le seguenti librerie Python:

- `bson`: Utilizzata per gestire gli identificatori ObjectId nel database MongoDB.
- `pymongo`: Utilizzata per interagire con il database MongoDB.
- `geopy.geocoders`: Utilizzata per ottenere informazioni di geolocalizzazione.
- `geopy.distance`: Utilizzata per calcolare la distanza tra le coordinate geografiche.
- `datetime`: Utilizzata per gestire date e orari.
- `functools.partial`: Utilizzata per creare funzioni parziali.

## Funzionalità Principali ✅

Il programma si suddivide nelle seguenti fasi:

1. **Login**: Gli utenti possono accedere all'app inserendo il proprio nickname. Se il nickname non esiste, verrà creato un nuovo utente.
2. **Scelte**: Dopo il login, gli utenti possono effettuare una delle seguenti scelte:
   - **0. Biglietti Acquistati**: Gli utenti possono visualizzare i biglietti che hanno acquistato.
   - **1. Acquistare Biglietti**: Gli utenti possono cercare e acquistare biglietti per i concerti. Possono filtrare i concerti per nome dell'artista, nome del concerto, prezzo e geolocalizzazione. In alternativa, possono acquistare un biglietto specificando l'ID univoco del concerto. È possibile acquistare tutti i biglietti disponibili fino all'esaurimento delle scorte.
   - **2. Uscire**: Gli utenti possono uscire dal programma.
   

## Utilizzo 🛠️

1. Installa le librerie necessarie utilizzando il comando `pip install -r requirements.txt`.
2. Configura il database MongoDB e le credenziali di accesso nel file `.env`.
3. Esegui il programma Python utilizzando il comando `python main.py`.
4. Segui le istruzioni sul terminale per accedere e utilizzare l'app.

## Contributi 😁

Sono benvenuti contributi, suggerimenti e segnalazioni di bug. Per favore, apri un problema o invia una richiesta pull se desideri contribuire al progetto.

## Autore 🌟

Programma Biglietti Concerto è stato sviluppato da Davide Soltys, Matteo Civita, Mattia Rossini e Nicolo Ballabio.

## Licenza 📝

Questo progetto è concesso in licenza sotto MIT. Per ulteriori informazioni, consulta il file LICENSE.
