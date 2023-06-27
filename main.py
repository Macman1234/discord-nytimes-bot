import discord

import certifi
ca = certifi.where()

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import parsegames
import db
import creds

if __name__ == "__main__":
    # Create a MongoDB Client
    uri = creds.dburi
    # Create a new client and connect to the server
    dbclient = MongoClient(uri, tlsCAFile=ca, server_api=ServerApi('1'))
    
    intents = discord.Intents.default()
    intents.message_content = True

    bot = discord.Bot(intents=intents)
    
    @bot.event
    async def on_message(message):
        if db.validate_opt(dbclient, message.author):
            entry = parsegames.parse(message)
            if entry: db.add_entry(dbclient,entry)
            
    @bot.slash_command(guild_ids=creds.guilds)
    async def opt_in(ctx):
        code = db.opt_in_user(dbclient,ctx.author)
        if code == 1: await ctx.respond("You're opted into game tracking!")
        elif code == 2: await ctx.respond("You were already opted into game tracking. Nerd.")
        else: await ctx.respond("An error occured. Go pester Mac.")
        
    @bot.slash_command(guild_ids=creds.guilds)
    async def opt_out(ctx):
        code = db.opt_out_user(dbclient,ctx.author)
        if code == 1: await ctx.respond("You're opted out of game tracking!")
        elif code == 2: await ctx.respond("You're not yet opted into game tracking. Nerd.")
        else: await ctx.respond("An error occured. Go pester Mac.")
            
    bot.run(creds.discordtoken)