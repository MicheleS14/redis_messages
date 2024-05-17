import redis
import datetime

class Chat:
    def __init__(self):
        self.db = redis.Redis(host='localhost', port=16036, db=0)
        self.users_key = 'chat_users'
        self.messages_key = 'chat_messages'
        self.contacts_key_prefix = 'user_contacts:'
        self.dnd_key_prefix = 'user_dnd:'

    def register_user(self, username, password):
        if self.db.hexists(self.users_key, username):
            print(f"Username '{username}' already exists.")
            return

        self.db.hset(self.users_key, username, password)
        print(f"User '{username}' registered successfully.")

    def login(self, username, password):
        if not self.db.hexists(self.users_key, username):
            print(f"Username '{username}' does not exist.")
            return False

        stored_password = self.db.hget(self.users_key, username).decode()
        if password == stored_password:
            print(f"User '{username}' logged in successfully.")
            return True
        else:
            print("Invalid password.")
            return False

    def search_users(self, query):
        usernames = self.db.hkeys(self.users_key)
        usernames = [username.decode() for username in usernames]
        matching_users = [username for username in usernames if query.lower() in username.lower()]
        return matching_users

    def add_contact(self, username, contact_username):
        if not self.db.hexists(self.users_key, contact_username):
            print(f"Username '{contact_username}' does not exist.")
            return

        contacts_key = self.contacts_key_prefix + username
        self.db.sadd(contacts_key, contact_username)
        print(f"User '{contact_username}' added to contacts.")

    def set_dnd_mode(self, username, dnd_mode):
        dnd_key = self.dnd_key_prefix + username
        if dnd_mode:
            self.db.set(dnd_key, 1)
            print(f"User '{username}' is in Do Not Disturb mode.")
        else:
            self.db.delete(dnd_key)
            print(f"User '{username}' is not in Do Not Disturb mode.")

    def send_message(self, sender_username, recipient_username, message):
        if not self.db.hexists(self.users_key, recipient_username):
            print(f"Recipient username '{recipient_username}' does not exist.")
            return

        dnd_key = self.dnd_key_prefix + recipient_username
        if self.db.exists(dnd_key):
            print(f"Message cannot be delivered. '{recipient_username}' is in Do Not Disturb mode.")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_data = f"{sender_username}: {message} [{timestamp}]"
        chat_key = f"chat:{sender_username}:{recipient_username}"
        self.db.lpush(chat_key, message_data)
        print("Message sent successfully.")

    def get_chat_messages(self, username, other_username):
        chat_key = f"chat:{username}:{other_username}"
        messages = self.db.lrange(chat_key, 0, -1)
        messages = [message.decode() for message in messages]
        return messages

# Esempio di utilizzo
chat = Chat()

chat.register_user('Alice', 'password1')
chat.register_user('Bob', 'password2')
chat.register_user('Charlie', 'password3')

chat.login('Alice', 'password1')
chat.login('Bob', 'wrong_password')

matching_users = chat.search_users('a')
print("Matching users:")
for user in matching_users:
    print(user)

chat.add_contact('Alice', 'Bob')
chat.add_contact('Alice', 'Charlie')
chat.add_contact('Alice', 'David')  # Tentativo di aggiungere un utente inesistente

chat.set_dnd_mode('Bob', True)
chat.set_dnd_mode('Charlie', False)

chat.send_message('Alice', 'Bob', 'Ciao Bob!')
chat.send_message('Alice', 'Charlie', 'Ciao Charlie!')
chat.send_message('Alice', 'David', 'Ciao David!')  # Tentativo di inviare un messaggio a un utente inesistente

messages = chat.get_chat_messages('Alice', 'Bob')
print("Chat with Bob:")
for message in messages:
    print(message)

messages = chat.get_chat_messages('Alice', 'Charlie')
print("Chat with Charlie:")
for message in messages:
    print(message)