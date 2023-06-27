import discord
import certifi
ca = certifi.where()
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import parsegames
import db
import creds

class MyClient(discord.Client):
    def __init__(self) -> None:
        # needs message content intent
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        
        # Create a MongoDB Client
        uri = creds.dburi
        # Create a new client and connect to the server
        self.dbclient = MongoClient(uri, tlsCAFile=ca, server_api=ServerApi('1'))

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        # Send a ping to confirm a successful connection to DB
        try:
            self.dbclient.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
            
    async def on_message(self, message):
        if message.content.startswith('!gamesoptout'):
            db.opt_out_user(self.dbclient, message)
            await message.channel.send(f"{message.author.mention}, you've been opted out!")
        if message.content.startswith('!gamesoptin'):
            db.opt_in_user(self.dbclient, message)
            await message.channel.send(f"{message.author.mention}, you've been opted in!")
            
        if db.validate_opt(self.dbclient, message):
            entry = parsegames.parse(message)
            if entry: db.add_entry(self.dbclient,entry)
            if self.user in message.mentions:
                await message.channel.send("who, me?")

if __name__ == "__main__":
    client = MyClient()
    client.run(creds.discordtoken)