import discord
from discord.ext import commands
from Utils import Utils, Word


def get_langs(server):
    return sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Connait")])


def get_role_learn(server, lang):
    return discord.utils.get(server.roles, name=f'Apprend {lang}')


def get_role_know(server, lang):
    return discord.utils.get(server.roles, name=f'Connait {lang}')


def enum(people):
    return f"`{'`, `'.join(people[:-1])}` et `{people[-1]}`."


class Languages(commands.Cog):
    """
        Languages's command.
        Attributes:
            bot: the bot's instance. [Bot]
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ilearn(self, context, *args):
        """
            Se donner le rôle "Apprends" pour une langue.
            Parameters:
                context: the context in which the message is sent. [Message]
                args[0]: language's name. [Str]
        """
        # Vérifie que la commande à au moins un argument
        if await Utils.enough_args(len(args), 1, self.bot):
            server = context.message.guild
            lang = Word.normalize(args[0])
            # Vérifie si le language est sur le serveur.
            if lang in get_langs(server):
                await context.message.author.remove_roles(get_role_know(server, lang))
                await context.message.author.add_roles(get_role_learn(server, lang))
                await context.channel.send(f'Tu apprends la langue **{lang}**.')
            else:
                await context.channel.send(f'La langue **{lang}** est inconnue.')

    @commands.command(pass_context=True)
    async def iknow(self, context, *args):
        """
            Se donner le rôle "Connait" pour une langue.
            Parameters:
                context: the context in which the message is sent. [Message]
                args[0]: language's name. [Str]
        """
        # Vérifie que la commande à au moins un argument
        if await Utils.enough_args(len(args), 1, self.bot):
            server = context.message.guild
            lang = Word.normalize(args[0])
            # Vérifie si le language est sur le serveur.
            if lang in get_langs(server):
                await context.message.author.remove_roles(get_role_learn(server, lang))
                await context.message.author.add_roles(get_role_know(server, lang))
                await context.channel.send(f'Tu connais la langue **{lang}**.')
            else:
                await context.channel.send(f'La langue **{lang}** est inconnue.')

    @commands.command(pass_context=True)
    async def forget(self, context, *args):
        """Oublier une certaines langue."""
        # Vérifie que la commande à au moins un argument
        if await Utils.enough_args(len(args), 1, self.bot):
            server = context.message.guild
            lang = Word.normalize(args[0])
            # Vérifie si le language est sur le serveur.
            if lang in get_langs(server):
                await context.message.author.remove_roles(get_role_know(server, lang), get_role_learn(server, lang))
                await context.channel.send(f'Tu as oublié la langue **{lang}**.')
            else:
                await context.channel.send(f'La langue **{lang}** est inconnue.')

    @commands.command(pass_context=True)
    async def newlang(self, context, *args):
        """[MOD ONLY] Ajouter une langue."""
        # Vérifie que l'auteur est modérateur et qu'il y au moins un argument.
        if await Utils.is_moderator(context, self.bot) and await Utils.enough_args(len(args), 1, self.bot):
            server = context.message.guild
            lang = Word.normalize(args[0])
            # Vérifie si le language est sur le serveur.
            if lang not in get_langs(server):
                await server.create_role(name=f'Apprend {lang}')
                await server.create_role(name=f'Connait {lang}')
                await context.channel.send(f'La langue **{lang}** vient d\'être ajouter !')
            else:
                await context.channel.send(f'La langue **{lang}** est déjà connue.')

    @commands.command(pass_context=True)
    async def rmvlang(self, context, *args):
        """[MOD ONLY] Supprimer une langue."""
        # Vérifie que l'auteur est modérateur et qu'il y au moins un argument.
        if await Utils.is_moderator(context, self.bot) and await Utils.enough_args(len(args), 1, self.bot):
            server = context.message.guild
            lang = Word.normalize(args[0])
            # Vérifie si le language est sur le serveur.
            if lang in get_langs(server):
                await get_role_know(server, lang).delete()
                await get_role_learn(server, lang).delete()
                await context.channel.send(f'La langue **{lang}** vient d\'être supprimer !')
            else:
                await context.channel.send(f'La langue **{lang}** est inconnue.')

    @commands.command(pass_context=True)
    async def speakers(self, context, *args):
        """Afficher la liste des gens qui connaissent une certaine langue."""
        # Vérifie que la commande à au moins un argument
        if await Utils.enough_args(len(args), 1, self.bot):
            server = context.message.guild
            lang = Word.normalize(args[0])
            speakers = sorted([user.name for user in server.members if (get_role_know(server, lang) in user.roles)])
            # Vérifie si le language est sur le serveur.
            if lang in get_langs(server):
                if len(speakers) == 0:
                    await context.channel.send(f"Personne ne connait la langue **{lang}**.")
                elif len(speakers) == 1:
                    await context.channel.send(f"Une seule personne connait la langue **{lang}**: {speakers[0]}.")
                else:
                    await context.channel.send(f"Ces personnes connaissent la langue **{lang}**: {enum(speakers)}")
            else:
                await context.channel.send(f'La langue **{lang}** est inconnue.')

    @commands.command(pass_context=True)
    async def learners(self, context, *args):
        """Afficher la liste des gens qui apprennent une certaine langue."""
        # Vérifie que la commande à au moins un argument
        if await Utils.enough_args(len(args), 1, self.bot):
            server = context.message.guild
            lang = Word.normalize(args[0])
            learners = sorted([user.name for user in server.members if (get_role_learn(server, lang) in user.roles)])
            # Vérifie si le language est sur le serveur
            if lang in get_langs(server):
                if len(learners) == 0:
                    await context.channel.send(f"Personne n'apprends la langue **{lang}**.")
                elif len(learners) == 1:
                    await context.channel.send(f"Une seule personne apprends la langue **{lang}**: `{learners[0]}`.")
                else:
                    await context.channel.send(f"Ces personnes apprennent la langue **{lang}**: {enum(learners)}")
            else:
                await context.channel.send(f'La langue **{lang}** est inconnue.')

    @commands.command(pass_context=True)
    async def langs(self, context):
        """Afficher la liste des langages du serveur."""
        languages = get_langs(context.message.guild)
        await context.channel.send(f'Le serveur gère les {len(languages)} langue(s) suivantes : {enum(languages)}')
