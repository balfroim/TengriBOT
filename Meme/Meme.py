from discord.ext import commands
import sqlite3
from Utils import Utils, DatabaseCommunicator


class Meme:
    """
        Memes.
        Attributes:
            bot: the bot's instance. [Bot]
            db_comm: the database communicator. [DatabaseCommunicator]
    """

    def __init__(self, bot):
        self.bot = bot
        self.db_comm = DatabaseCommunicator('Meme/meme.db', 'meme', 'name TEXT, url TEXT, desc TEXT')

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
            url = self.db_comm.select_w_cdt('url', f'name={name}')
            # Display the url if the meme exist
            if url != list():
                await self.bot.say(url[0][0])
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
            meme_already_exists = self.db_comm.select_w_cdt('*', f'name={name}') != list()
            # Communicate with the database
            if not meme_already_exists:
                self.db_comm.insert((name, url, desc))
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
            meme_already_exists = self.db_comm.select_w_cdt('*', f'name={name}') != list()
            if meme_already_exists:
                self.db_comm.deletefrom(f'name={name}')
                await self.bot.say(f'Le meme "{name}" a été supprimé.')
            else:
                await self.bot.say(f'Le meme "{name}" n\'existais pas.')

    @commands.command()
    async def memelist(self):
        """Display the meme list."""
        # Get all the memes
        mmlist = self.db_comm.select('name, url, desc')
        # Check if the list not empty
        if mmlist is not None:
            # Create the message to display
            message = '```Markdown\n' + '\n'.join([f'* {name}: {desc}' for (name, url, desc) in mmlist]) + '\n```'
            await self.bot.say(message)
        else:
            await self.bot.say('Il n\'y a aucun meme.')
