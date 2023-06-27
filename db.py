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

def opt_in_user(client,username):
    return

def opt_out_user(client,username):
    return

def validate_opt(client,username):
    if TESTING: return True
    return

if __name__ == "__main__":
    import certifi
    import creds
    ca = certifi.where()
    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi

    uri = creds.dburi
    # Create a new client and connect to the server
    client = MongoClient(uri, tlsCAFile=ca, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    #add_entry(client,example_score)
    
    entries = get_entries_by_ID(client,1)
    for item in entries:
    # This does not give a very readable output
        print(item)