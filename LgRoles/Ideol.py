import discord
from discord.ext import commands
from Utils import Word

class Ideol:
    """
        Commands related to the "Ideolinguist" role
        Attributes:
            bot: the bot's instance. [Bot]
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ideolist(self, context):
        """
            Display the list of "Ideolinguist".
            Parameters:
                context: the context in which the message is sent. [Message]
        """
        data = IdeolData(context)
        ideol_list = sorted([user.name for user in data.server.members if (data.ideol_role in user.roles)])
        if len(ideol_list) > 1:
            message = f'Il y a {nb_ideol} idéolinguistes sur ce serveur : '
            message += ', '.join(ideol_list[:-1]) + f' et {ideol_list[-1]}.'
            await self.bot.say(message)
        elif len(ideol_list) == 1:
            await self.bot.say(f'Le seul idéolinguiste du serveur est {ideol_list[0]}.')
        else:
            await self.bot.say('Il n\'y as pas d\'idéolinguiste')

    @commands.command(pass_context=True)
    async def ideol(self, context):
        """
            Add the badge "Ideolinguist" to the author.
            Parameters:
                context: the context in which the message is sent. [Message]
        """
        data = IdeolData(context)
        if data.ideol_role not in data.author.roles:
            await self.bot.add_roles(data.author, data.ideol_role)
            await self.bot.say('Tu es maintenant idéolinguiste !')
        else:
            await self.bot.say('Tu étais déjà idéolinguiste !')

    @commands.command(pass_context=True)
    async def rmvideol(self, context):
        """
            Remove the badge "Ideolinguist" to the author.
            Parameters:
                context: the context in which the message is sent. [Message]
        """
        data = IdeolData(context)
        if data.ideol_role in data.author.roles:
            await self.bot.remove_roles(data.author, data.ideol_role)
            await self.bot.say('Tu n\'es plus idéolinguiste !')
        else:
            await self.bot.say('Tu n\'étais pas idéolinguiste !')


class IdeolData:
    """
        Contains useful data for the Ideol class
        Attributes:
            server: the server in which the command was executed. [Server]
            author: the user who executed the command. [Client]
            role: the "Ideolinguist" role. [Role]

    """
    def __init__(self, context):
        self.server = context.message.server
        self.author = context.message.author
        self.ideol_role = discord.utils.get(self.server.roles, name='Idéolinguiste')