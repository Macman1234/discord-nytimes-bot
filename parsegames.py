import re
from dateutil import parser
from collections import namedtuple
import discord
from datetime import datetime

def parse(message: discord.Message):
    # check if nytimes mini
    if re.search("https:\/\/www.nytimes.com\/badges\/games\/mini.html",message.content):
        discordID = message.author.id
        gamename = "nytimesmini"
        try: 
            gamedate = parser.parse(re.search("(?:d=)(.+?)(?=&)",message.content)[1])
            score = re.search("(?:\&t=)(.+?)(?=&)",message.content)[1]
            timestamp = message.created_at
            entry = {
                "discord_ID" : discordID,
                "game_name" : gamename,
                "game_date" : gamedate,
                "score" : score,
                "timestamp" : timestamp
            }
            return entry
        except:
            #print("error in parsing mini crossword")
            return None
    # check if Connections
    # check if Wordle
    # check if []
    return None

if __name__ == "__main__":
    # create example message
    message = discord.Message
    message.content = "https://www.nytimes.com/badges/games/mini.html?d=2023-06-19&t=75&c=844bfb2269ebe3f4b8d0a17f977f20f1&smid=url-share"
    message.author = discord.Member
    message.author.id = 1111
    message.created_at = datetime.now()
    print(parse(message))