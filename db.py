# holds the database methods
from dateutil import parser as dateparser

# add entry
TESTING = True

def add_entry(client,entry):
    if TESTING: db = client['scoresdbtest']
    else: db = client['scoresdb']
    scores = db['scores']
    scores.insert_one(entry)
    print(entry)
    return

# get entries
def get_entries_by_ID(client,ID):
    if TESTING: db = client['scoresdbtest']
    else: db = client['scoresdb']
    scores = db['scores']
    return(scores.find({"discordID" : ID}))

def opt_in_user(client,author):
    if TESTING: db = client['usersdbtest']
    else: db = client['usersdb']
    users = db['users']
    if users.find_one({"id":author.id}): return 2
    else:
        users.insert_one({"id":author.id})
        return 1

def opt_out_user(client,author):
    if TESTING: db = client['usersdbtest']
    else: db = client['usersdb']
    users = db['users']
    if users.find_one({"id":author.id}):
        users.delete_one({"id":author.id})
        return 1
    else: return 2

def validate_opt(client,author):
    if TESTING: db = client['usersdbtest']
    else: db = client['usersdb']
    users = db['users']
    if users.find_one({"id":author.id}): return True
    else: return False