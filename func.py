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

def aggiungi_utente(user):
    # Controlla se l'utente esiste già nei contatti
    if not r.sismember('contacts', user):
        # Aggiungi l'utente ai contatti
        r.sadd('contacts', user)
    else:
        print(f"L'utente {user} è già nei tuoi contatti.")
        
        
def ricerca_utenti():
    query = input("Inserisci il nome utente (anche parziale): ").lower()
    
    # Cerco gli utenti che corrispondono alla query
    users = r.keys(query + "*")
    
    if not users:
        print("Nessun utente trovato.")
    else:
        print("Utenti trovati:")
        for i, user in enumerate(users, 1):
            print(f'{i}. {user.encode()}')
        
        while True:
            try:
                selection = int(input("Seleziona un utente da aggiungere(o premi 0 per uscire): "))
                if selection == 0:
                    return
                elif 1 <= selection <= len(users):
                    selected_user = users[selection - 1].encode()
                    break
                else:
                    print("Selezione non valida. Riprova.")
            except ValueError:
                print("Inserisci un numero valido.")
        
        aggiungi_utente(selected_user)
        print(f"L'utente {selected_user} è stato aggiunto ai tuoi contatti.")

def impostazione_dnd(username):
    # Verifica lo stato attuale della modalità DND
    stato_dnd = r.hget(username, "dnd")
    
    # Se la modalità DND è già attiva, chiedi all'utente se vuole disattivarla
    if stato_dnd == 'True':
        risp = input("Modalità dnd attualmente attiva, vuoi disattivarla? (Y/N): ")
        if risp.lower() == 'y':
            dnd = 'False'
            r.hset(username, "dnd", dnd)
            print("***Modalità Do Not Disturb disattivata***")
        else:
            print("***Modalità Do Not Disturb rimane attiva***")
    # Altrimenti, chiedi all'utente se vuole attivare la modalità DND
    else:
        risp = input("Vuoi attivare la modalità Do Not Disturb? (Y/N): \n(Se sceglierai di si non potrai ricevere messaggi da altri utenti)\n")
        if risp.lower() == 'y':
            dnd = 'True'
            r.hset(username, "dnd", dnd)
            print("***Modalità Do Not Disturb attivata***")
        elif risp.lower() == 'n':
            dnd = 'False'
            r.hset(username, "dnd", dnd)
            print("***Modalità Do Not Disturb disattivata***")

  
def invia_mess():
    print('da fare')

def leggi_mess():
    print('da fare')
