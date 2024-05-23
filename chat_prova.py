import redis
import datetime
import func


# Connessione a Redis
r = redis.Redis(host='redis-16036.c250.eu-central-1-1.ec2.redns.redis-cloud.com', port=16036, db=0, username='default', password='69Fa488VqsGKuseTkFy5uwVlupgDBF2V', decode_responses=True)

if __name__ == '__main__':
    utente_corrente = None
    
    while True:
        print("\n*** Benvenuto nella chat ***")
        print("1. Login")
        print("2. Registrazione")
        print("0. Esci")
        
        scelta = input('scelta: ')
        
        if scelta == "1":
            utente_corrente = func.login()
            if utente_corrente:
                break
        elif scelta == "2":
            func.registrazione()
        elif scelta == "0":
            print("Grazie per aver utilizzato la chat. Arrivederci!")
            break
        else:
            print("Scelta non valida. Riprova.")

    if utente_corrente:
        while True:
            print(f"\n*** Benvenuto nella chat, {utente_corrente}!***")
            print("1. Ricerca e aggiungi contatti")
            print("2. Imposta modalità Do Not Disturb")
            print("3. Chatta")
            print("0. Esci")

            scelta = input("Scelta: ")

            if scelta == "1":
                func.ricerca_utenti(utente_corrente)
            elif scelta == "2":
                func.impostazione_dnd(utente_corrente)
            elif scelta == "3":
                func.seleziona_chat(utente_corrente)
            elif scelta == "0":
                print("Grazie per aver utilizzato la chat. Arrivederci!")
                break
            else:
                print("Scelta non valida. Riprova.")
    else:
        print("Impossibile accedere alla chat. Riprova.")
