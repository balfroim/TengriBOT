import discord
from discord.ext import commands


class Ideol(commands.Cog):
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
        server = context.message.guild
        channel = context.message.channel
        ideol_role = discord.utils.get(server.roles, name='Idéolinguiste')
        ideol_list = sorted([user.name for user in server.members if (ideol_role in user.roles)])
        nb_ideol = len(ideol_list)
        if nb_ideol > 1:
            message = f'Il y a {nb_ideol} idéolinguistes sur ce serveur : '
            message += ', '.join(ideol_list[:-1]) + f' et {ideol_list[-1]}.'
            await channel.send(message)
        elif nb_ideol == 1:
            await channel.send(f'Le seul idéolinguiste du serveur est {ideol_list[0]}.')
        else:
            await channel.send('Il n\'y as pas d\'idéolinguiste')

    @commands.command(pass_context=True)
    async def ideol(self, context):
        """
            Add the badge "Ideolinguist" to the author.
            Parameters:
                context: the context in which the message is sent. [Message]
        """
        server = context.message.guild
        channel = context.message.channel
        author = context.message.author
        ideol_role = discord.utils.get(server.roles, name='Idéolinguiste')
        if ideol_role not in author.roles:
            await author.add_roles(ideol_role)
            await channel.send('Tu es maintenant idéolinguiste !')
        else:
            await channel.send('Tu étais déjà idéolinguiste !')

    @commands.command(pass_context=True)
    async def rmvideol(self, context):
        """
            Remove the badge "Ideolinguist" to the author.
            Parameters:
                context: the context in which the message is sent. [Message]
        """
        server = context.message.guild
        channel = context.message.channel
        author = context.message.author
        ideol_role = discord.utils.get(server.roles, name='Idéolinguiste')
        if ideol_role in author.roles:
            await author.remove_roles(ideol_role)
            await channel.send('Tu n\'es plus idéolinguiste !')
        else:
            await channel.send('Tu n\'étais pas idéolinguiste !')