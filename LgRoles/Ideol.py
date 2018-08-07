import discord
from discord.ext import commands


class Ideol:
    """Commandes relative aux idéolinguistes"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ideolist(self, context):
        """Donne la liste des idéolinguistes"""
        # The server in which the command was executed
        server = context.message.server
        # The role of ideolinguist
        ideol_role = discord.utils.get(server.roles, name='Idéolinguiste')

        # The list of ideolinguists
        ideol_list = sorted([user.name for user in server.members if (ideol_role in user.roles)])
        # The number of ideolinguists
        nb_ideol = len(ideol_list)

        if nb_ideol > 1:
            message = f'Il y a {nb_ideol} idéolinguiste(s) sur ce serveur : '
            for ideolinguist in ideol_list[:-2]:
                message += f'{ideolinguist}, '
            message += f'{ideol_list[-2]} et {ideol_list[-1]}.'
            await self.bot.say(message)
        elif nb_ideol == 1:
            await self.bot.say(f'Le seul idéolinguiste du serveur est {ideol_list[0]}.')
        else:
            await self.bot.say('Il n\'y as pas d\'idéolinguiste')

    @commands.command(pass_context=True)
    async def ideol(self, context):
        """Ajoute le badge ideolinguiste"""
        # The server in which the command was executed
        server = context.message.server
        # The user who executed the command
        author = context.message.author
        # The role of ideolinguist
        ideol_role = discord.utils.get(server.roles, name='Idéolinguiste')

        if not (ideol_role in author.roles):
            await self.bot.add_roles(author, ideol_role)
            await self.bot.say('Tu es maintenant idéolinguiste !')
        else:
            await self.bot.say('Tu étais déjà idéolinguiste !')

    @commands.command(pass_context=True)
    async def rmvideol(self, context):
        """Retire le badge ideolinguiste"""
        # The server in which the command was executed
        server = context.message.server
        # The user who executed the command
        author = context.message.author
        # The role of ideolinguist
        ideol_role = discord.utils.get(server.roles, name='Idéolinguiste')

        if ideol_role in author.roles:
            await self.bot.remove_roles(author, ideol_role)
            await self.bot.say('Tu n\'es plus idéolinguiste !')
        else:
            await self.bot.say('Tu n\'étais pas idéolinguiste !')

