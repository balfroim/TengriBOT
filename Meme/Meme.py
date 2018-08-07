from discord.ext import commands
import sqlite3
from Utils import Utils


class Meme:
    """
        Memes.
        Attributes:
            bot: the bot's instance. [Bot]
    """

    def __init__(self, bot):
        self.bot = bot
        # Create the meme data base if not exists
        createMemeDb = """CREATE TABLE IF NOT EXISTS meme(name TEXT,url TEXT,desc TEXT);"""
        with sqlite3.connect('Meme/meme.db') as conn:
            cursor = conn.cursor()
            cursor.execute(createMemeDb)
            conn.commit()

    @commands.command()
    async def meme(self, *args):
        """
            Display a meme.
            Parameters:
                args[0] : meme's name.
        """
        # Check if the command has enough arguments
        if await Utils.enough_args(len(args), 1, self.bot):
            name = args[0].lower()
            # Make a request to the database
            with sqlite3.connect('Meme/meme.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT url FROM meme WHERE name = ?;", (name,))
                url = cursor.fetchone()
            # Display the url if the meme exist
            if url is not None:
                await self.bot.say(url[0])
            else:
                await self.bot.say(f'Désolé, je ne connais pas le meme "{name}"')

    @commands.command(pass_context=True)
    async def memeadd(self, context, *args):
        """
            [MOD ONLY] Add a meme to database.
            Parameters
            ----------
                args[0]: meme's name. [str]
                args[1]: meme's url. [str]
                args[2:]: meme's description. [str]
        """
        # Check if the author is a moderator
        # Check if the command has enough arguments
        if await Utils.is_moderator(context, self.bot) and await Utils.enough_args(len(args), 3, self.bot):
            name = args[0].lower()
            url = args[1]
            desc = ' '.join(args[2:])
            # Communicate with the database
            with sqlite3.connect('Meme/meme.db') as conn:
                cursor = conn.cursor()
                # Check if the meme already exist
                cursor.execute("SELECT * FROM meme WHERE name = ?", (name,))
                if cursor.fetchone() is None:
                    # Add the meme to the database
                    cursor.execute("INSERT INTO meme VALUES (?, ?, ?);", (name, url, desc))
                    conn.commit()
                    await self.bot.say(f'Le meme "{name}" a été ajouté avec l\'url : {url}')
                else:
                    await self.bot.say(f'Le meme "{name}" existe déjà')

    @commands.command(pass_context=True)
    async def memermv(self, context, *args):
        """
            [MOD ONLY] Remove a meme from database.
            Parameters
            ----------
                args[0]: meme's name. [str]
        """
        # Check if the author is a moderator
        # Check if the command have enough arguments
        if await Utils.is_moderator(context, self.bot) and await Utils.enough_args(len(args), 1, self.bot):
            name = args[0].lower()
            # Communicate with the database
            with sqlite3.connect('Meme/meme.db') as conn:
                cursor = conn.cursor()
                # Check if the meme already exist
                cursor.execute("SELECT * FROM meme WHERE name = ?", (name,))
                if cursor.fetchone() is not None:
                    # Remove the meme from the database
                    cursor.execute("DELETE FROM meme WHERE name=?;", (name,))
                    conn.commit()
                    await self.bot.say(f'Le meme "{name}" a été supprimé.')
                else:
                    await self.bot.say(f'Le meme "{name}" n\'existais pas.')

    @commands.command()
    async def memelist(self):
        """Display the meme list."""
        # Get all the memes
        with sqlite3.connect('Meme/meme.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, url, desc FROM meme;")
            mmlist = cursor.fetchall()
        # Check if the list not empty
        if mmlist is not None:
            # Create the message to display
            message = '```Markdown\n'
            for mm in mmlist:
                name, desc = mm[0], mm[2]
                message += f'* {name}: {desc}\n'
            message += '```'
            await self.bot.say(message)
        else:
            await self.bot.say('Il n\'y a aucun même.')
