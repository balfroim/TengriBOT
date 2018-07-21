import discord
from discord.ext import commands
import sys
import sqlite3


class Meme:
    """Commandes relatives aux memes"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, *args):
        """
            Affiche un meme
            $meme <name>
        """

        # check if it's the right length
        if len(args) == 1:
            name = args[0].lower()
        else:
            await self.bot.say(f'Il faut seulement 1 argument, pas {len(args)}.')
            return

        try:
            with sqlite3.connect('meme.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT url FROM meme WHERE name = ?;", (name,))
                url = cursor.fetchone()[0]
            await self.bot.say(url)
        except:
            await self.bot.say(f'Désolé il y a eu une erreur : {sys.exc_info()}')

    @commands.command(pass_context=True)
    async def memeadd(self, context, *args):
        """
            [MOD ONLY] Ajoute un même à la base de donnée
            $memeadd <name> <url> <desc>
        """
        author = context.message.author
        server = context.message.server
        # check if the author is a moderator
        isModerator = discord.utils.get(server.roles, name='Modération') in author.roles
        if not isModerator:
            await self.bot.say('Seul les modérateurs peuvent utiliser cette commande')
            return

        # check if it's the right length
        if len(args) >= 3:
            name = args[0].lower()
            url = args[1]
            desc = str()
            for word in args[2:-1]:
                desc += f'{word} '
            desc += args[-1]
        else:
            await self.bot.say(f'Il faut au moins 3 arguments, pas {len(args)}.')
            return

        try:
            with sqlite3.connect('meme.db') as conn:
                cursor = conn.cursor()
                # Check if the meme already exist
                cursor.execute("SELECT * FROM meme WHERE name = ?", (name,))
                if cursor.fetchone() is not None:
                    await self.bot.say(f'Le meme "{name}" existe déjà')
                    return
                # Create the meme in the database
                cursor.execute("INSERT INTO meme VALUES (?, ?, ?);", (name, url, desc))
                conn.commit()
            await self.bot.say(f'Le meme "{name}" a été ajouté avec l\'url : {url}')
        except:
            await self.bot.say(f'Désolé il y a eu une erreur : {sys.exc_info()}')

    @commands.command(pass_context=True)
    async def memermv(self, context, *args):
        """
            [MOD ONLY] Retire un même à la base de donnée
            $memermv <name>
        """
        author = context.message.author
        server = context.message.server
        # check if the author is a moderator
        isModerator = discord.utils.get(server.roles, name='Modération') in author.roles
        if not isModerator:
            await self.bot.say('Seul les modérateurs peuvent utiliser cette commande')
            return

        # check if it's the right length
        if len(args) == 1:
            name = args[0].lower()
        else:
            await self.bot.say(f'Il faut seulement 1 argument, pas {len(args)}.')
            return

        try:
            with sqlite3.connect('meme.db') as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM meme WHERE name=?;", (name,))
                conn.commit()
            await self.bot.say(f'Le meme "{name}" a été supprimé.')
        except:
            await self.bot.say(f'Désolé il y a eu une erreur : {sys.exc_info()}')

    @commands.command()
    async def memelist(self):
        """Affiche la liste des mêmes"""
        try:
            with sqlite3.connect('meme.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name, url, desc FROM meme;")
                mmlist = cursor.fetchall()
            if len(mmlist) == 0:
                await self.bot.say('Il n\'y a aucun même.')
            else:
                # Liste des mêmes
                message = '```Markdown\n'
                for mm in mmlist:
                    name, desc = mm[0], mm[2]
                    message += f'* {name}: {desc}\n'
                message += '```'
                await self.bot.say(message)
        except:
            await self.bot.say(f'Désolé il y a eu une erreur : {sys.exc_info()}')