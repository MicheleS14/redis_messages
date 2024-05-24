#Questo è un altro metodo pensato per la ricerca degi uteti 
#con la possibilità di registrarsi con lo stesso nome ma con caratteri diversi 


#user = username.lower()
 #r.hset(username, "username", user)
""" 
Ricerca del user
    if not r.exists(username, user):
        r.set(user, username)
    else:
        r.sadd(user, username)
"""