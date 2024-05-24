import redis
import datetime
import json

# Connessione a Redis
r = redis.Redis(host='redis-16036.c250.eu-central-1-1.ec2.redns.redis-cloud.com', port=16036, db=0, username='default', password='69Fa488VqsGKuseTkFy5uwVlupgDBF2V', decode_responses=True)

def registrazione():
    username = input("Inserisci il nome utente: ").lower()
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
    username = input("Inserisci il nome utente: ").lower()
    password = input("Inserisci la password: ")
    
    # Controllo le credenziali dell'utente
    if r.hget(username, "password") == password:
        print("Accesso consentito.")
        return username
    else:
        print("Credenziali errate.")
        return None

def aggiungi_utente(user, utente_corrente):
    # Controlla se l'utente esiste già nei contatti dell'utente corrente
    if not r.sismember(f"contacts:{utente_corrente}", user):
        # Aggiungi l'utente ai contatti dell'utente corrente
        r.sadd(f"contacts:{utente_corrente}", user)
        print(f"L'utente {user} è stato aggiunto ai contatti.")
    else:
        print(f"L'utente {user} è già nei tuoi contatti.")

def ricerca_utenti(utente_corrente):
    query = input("Inserisci il nome utente (anche parziale): ").lower()
    
    # Cerco gli utenti che corrispondono alla query
    users = r.keys(query + "*")
    
    if not users:
        print("Nessun utente trovato.")
    else:
        print("Utenti trovati:")
        for i, user in enumerate(users, 1):
            print(f'{i}. {user}')
        
        while True:
            try:
                selection = int(input("Seleziona un utente da aggiungere (o premi 0 per uscire): "))
                if selection == 0:
                    return
                elif 1 <= selection <= len(users):
                    selected_user = users[selection - 1]
                    aggiungi_utente(selected_user, utente_corrente)
                    break
                else:
                    print("Selezione non valida. Riprova.")
            except ValueError:
                print("Inserisci un numero valido.")

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
        risp = input("Vuoi attivare la modalità Do Not Disturb? (Y/N): \n(Se sceglierai di sì non potrai ricevere messaggi da altri utenti)\n")
        if risp.lower() == 'y':
            dnd = 'True'
            r.hset(username, "dnd", dnd)
            print("***Modalità Do Not Disturb attivata***")
        elif risp.lower() == 'n':
            dnd = 'False'
            r.hset(username, "dnd", dnd)
            print("***Modalità Do Not Disturb disattivata***")

def get_contatti(utente_corrente):
    # Ottieni i contatti dell'utente corrente
    contatti = r.smembers(f"contacts:{utente_corrente}")
    return list(contatti)

# Selezione CHAT
def seleziona_chat(utente_corrente):
    contatti = get_contatti(utente_corrente)
    if not contatti:
        print("Non hai contatti. Aggiungi prima dei contatti per iniziare una chat.")
        return

    print("\n*** Seleziona un contatto per iniziare una chat ***")
    for i, contatto in enumerate(contatti, 1):
        print(f"{i}. {contatto}")
    
    while True:
        try:
            scelta = int(input("Seleziona un contatto (o premi 0 per uscire): "))
            if scelta == 0:
                return
            elif 1 <= scelta <= len(contatti):
                contatto_selezionato = contatti[scelta - 1]
                print(f"Iniziando una chat con {contatto_selezionato}...")
                chat(utente_corrente, contatto_selezionato)
                return
            else:
                print("Selezione non valida. Riprova.")
        except ValueError:
            print("Inserisci un numero valido.")

def chat(utente_corrente, contatto):
    while True:
        messaggio = input(f"{utente_corrente} (scrivi 'esc' per uscire): ")
        if messaggio.lower() == "esc":
            break
        else:
            invia_mess(utente_corrente, contatto, messaggio)
            leggi_mess(utente_corrente, contatto)

def invia_mess(utente_corrente, contatto, messaggio):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messaggio_data = {
        "from": utente_corrente,
        "to": contatto,
        "message": messaggio,
        "timestamp": timestamp
    }
    r.rpush(f"chat:{utente_corrente}:{contatto}", json.dumps(messaggio_data))
    r.rpush(f"chat:{contatto}:{utente_corrente}", json.dumps(messaggio_data))
    print("Messaggio inviato!")

def leggi_mess(utente_corrente, contatto):
    chiave_chat = f"chat:{utente_corrente}:{contatto}"
    messaggi = r.lrange(chiave_chat, 0, -1)
    if not messaggi:
        print("Nessun messaggio nella chat.")
    else:
        print("\n*** Messaggi nella chat con", contatto, "***")
        for messaggio in messaggi:
            data = json.loads(messaggio)
            direzione = ">" if data["from"] == utente_corrente else "<"
            print(f"{data['timestamp']} - {data['from']} {direzione} {data['message']}")
