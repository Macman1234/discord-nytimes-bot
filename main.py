import discord

import certifi
ca = certifi.where()

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import parsegames
import db
import config

if __name__ == "__main__":
    # Create a MongoDB Client
    uri = config.dburi
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
            
    @bot.slash_command(guild_ids=config.guilds)
    async def opt_in(ctx):
        code = db.opt_in_user(dbclient,ctx.author)
        if code == 1: await ctx.respond("You've opted into game tracking!")
        elif code == 2: await ctx.respond("You were already opted into game tracking. Nerd.")
        else: await ctx.respond("An error occured. Go pester Mac.")
        return
        
    @bot.slash_command(guild_ids=config.guilds)
    async def opt_out(ctx):
        code = db.opt_out_user(dbclient,ctx.author)
        if code == 1: await ctx.respond("You've opted out of game tracking!")
        elif code == 2: await ctx.respond("You're not yet opted into game tracking. Nerd.")
        else: await ctx.respond("An error occured. Go pester Mac.")
        return
        
    @bot.slash_command(guild_ids=config.guilds)
    async def list_scores(ctx,game,num):
        if not db.validate_opt(dbclient, ctx.author):
            await ctx.respond("silly goose, you gotta opt in before this works.")
            return
        if not num: num = 7
        games = list(config.games.keys())
        if not game in games:
            await ctx.respond(f"{game} is not a valid game. Current valid games are: {str(games)}")
            return
        else:
            results = db.get_entries(dbclient,ctx.author,game,num)
            resultString = ""
            for result in results:
                resultString += f"Date: {result['game_date']}, Score: {result['score']}\n"
            await ctx.respond(resultString)
            
    @bot.slash_command(guild_ids=config.guilds)
    async def trawl(ctx):
        if not db.validate_opt(dbclient, ctx.author):
            await ctx.respond("silly goose, you gotta opt in before this works.")
            return
        counter = 0
        await ctx.respond("Starting trawl through message history. If anyone sends a command before this is done it'll probably break something.")
        async for message in ctx.channel.history(limit=None):
            if message.author == ctx.author:
                entry = parsegames.parse(message)
                if entry: 
                    code = db.add_entry(dbclient,entry)
                    if code == 1: counter += 1
        await ctx.channel.send(f"Done! Added {counter} entries.")
    bot.run(config.discordtoken)