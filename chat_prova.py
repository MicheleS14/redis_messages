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
            print("\n*** Benvenuto nella chat ***")
            print("1. Ricerca utenti")
            print("2. Aggiungi contatto")
            print("3. Imposta modalità Do Not Disturb")
            print("4. Invia messaggio")
            print("5. Leggi chat")
            print("0. Esci")

            scelta = input("Scelta: ")

            if scelta == "1":
                func.ricerca_utenti()
            elif scelta == "2":
                func.aggiungi_contatto(utente_corrente)
            elif scelta == "3":
                func.impostazione_dnd(utente_corrente)
            elif scelta == "4":
                func.invia_mess(utente_corrente)
            elif scelta == "5":
                func.leggi_mess(utente_corrente)
            elif scelta == "0":
                print("Grazie per aver utilizzato la chat. Arrivederci!")
                break
            else:
                print("Scelta non valida. Riprova.")
    else:
        print("Impossibile accedere alla chat. Riprova.")
