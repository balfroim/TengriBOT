import discord
from discord.ext import commands
import sqlite3
from Ideol import Ideol
from Meme import Meme
from Lg import Lg

# Init the bot
bot = commands.Bot(command_prefix='$', description='Bot pour le Discord Linguisticae.')


@bot.event
async def on_ready():
    print('Logged in as %s' % bot.user.name)
    createMemeDb = """CREATE TABLE IF NOT EXISTS meme(name text,url text,desc text);"""
    with sqlite3.connect('meme.db') as conn:
        cursor = conn.cursor()
        cursor.execute(createMemeDb)
        conn.commit()

bot.add_cog(Ideol(bot))
bot.add_cog(Meme(bot))
bot.add_cog(Lg(bot))

# Read the token and run the bot
with open('token.txt', 'r') as token_file:
    token = token_file.readlines()[0].split(' ')[0]

bot.run(token)
