import redis
import datetime



# Connessione a Redis
r = redis.Redis(host='redis-16036.c250.eu-central-1-1.ec2.redns.redis-cloud.com', port=16036, db=0, username='default', password='69Fa488VqsGKuseTkFy5uwVlupgDBF2V', decode_responses=True)

def registrazione():
    username = input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")
    
    # Controllo se l'utente esiste già
    if r.exists(username):
        print("Utente già registrato.")
    else:
        # Salvo le informazioni dell'utente in Redis
        r.hset(username, "password", password)
        r.hset(username, "dnd", "False")
        print("Registrazione completata.")

# Funzione per effettuare il login
def login():
    username = input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")
    
    # Controllo le credenziali dell'utente
    if r.hget(username, "password") == password:
        print("Accesso consentito.")
        return username
    else:
        print("Credenziali errate.")
        return None

def ricerca_utenti():
    print('da fare')
    
def aggiungi_contatti():
    print('da fare')
    
def impostazione_dnd():
    print('da fare')
    
def invia_mess():
    print('da fare')

def leggi_mess():
    print('da fare')
