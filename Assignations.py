import discord
from discord.ext import commands


def get_langs(server):
    return sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Connait")])


def get_role_learn(server, lang):
    return discord.utils.get(server.roles, name=f'Apprend {lang}')


def get_role_know(server, lang):
    return discord.utils.get(server.roles, name=f'Connait {lang}')


def enum(people):
    return f"`{'`, `'.join(people[:-1])}` et `{people[-1]}`."


def normalize(word):
    """Normalize a word."""
    return word[0].upper() + word[1:].lower()


def is_moderator(context):
    """Check the author is a moderator."""
    modo_roles = {"igidarúren «prophètes»", "díngen «divinités»", "Admin"}
    return not modo_roles.isdisjoint({role.name for role in context.message.author.roles})


class Assignations(commands.Cog):
    """Commandes d'assignations"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ilearn(self, context, *args):
        """Assigner le rôle "Apprends" pour une langue."""
        # Vérifie que la commande à au moins un argument
        if len(args) >= 1:
            server = context.message.guild
            lang = normalize(args[0])
            # Vérifie si le language est sur le serveur.
            if lang in get_langs(server):
                await context.message.author.remove_roles(get_role_know(server, lang))
                await context.message.author.add_roles(get_role_learn(server, lang))
                await context.channel.send(f'Tu apprends la langue **{lang}**.')
            else:
                await context.channel.send(f'La langue **{lang}** est inconnue.')
        else:
            await context.channel.send("Il manque le nom de la langue.")

    @commands.command(pass_context=True)
    async def iknow(self, context, *args):
        """Assigner le rôle "Connait" pour une langue."""
        # Vérifie que la commande à au moins un argument
        if len(args) >= 1:
            server = context.message.guild
            lang = normalize(args[0])
            # Vérifie si le language est sur le serveur.
            if lang in get_langs(server):
                await context.message.author.remove_roles(get_role_learn(server, lang))
                await context.message.author.add_roles(get_role_know(server, lang))
                await context.channel.send(f'Tu connais la langue **{lang}**.')
            else:
                await context.channel.send(f'La langue **{lang}** est inconnue.')
        else:
            await context.channel.send("Il manque le nom de la langue.")

    @commands.command(pass_context=True)
    async def forget(self, context, *args):
        """Oublier une certaine langue."""
        # Vérifie que la commande à au moins un argument
        if len(args) >= 1:
            server = context.message.guild
            lang = normalize(args[0])
            # Vérifie si le language est sur le serveur.
            if lang in get_langs(server):
                await context.message.author.remove_roles(get_role_know(server, lang), get_role_learn(server, lang))
                await context.channel.send(f'Tu as oublié la langue **{lang}**.')
            else:
                await context.channel.send(f'La langue **{lang}** est inconnue.')
        else:
            await context.channel.send("Il manque le nom de la langue.")

    @commands.command(pass_context=True)
    async def newlang(self, context, *args):
        """[MOD ONLY] Ajouter une langue."""
        # Vérifie que l'auteur est modérateur et qu'il y au moins un argument.
        if is_moderator(context) and len(args) >= 1:
            server = context.message.guild
            lang = normalize(args[0])
            # Vérifie si le language est sur le serveur.
            if lang not in get_langs(server):
                await server.create_role(name=f'Apprend {lang}')
                await server.create_role(name=f'Connait {lang}')
                await context.channel.send(f'La langue **{lang}** vient d\'être ajouter !')
            else:
                await context.channel.send(f'La langue **{lang}** est déjà connue.')
                # Vérifie que la commande à au moins un argument
        else:
            await context.channel.send("Il manque le nom de la langue ou alors vous n'êtes pas modérateur.")

    @commands.command(pass_context=True)
    async def rmvlang(self, context, *args):
        """[MOD ONLY] Supprimer une langue."""
        # Vérifie que l'auteur est modérateur et qu'il y au moins un argument.
        if is_moderator(context) and len(args) >= 1:
            server = context.message.guild
            lang = normalize(args[0])
            # Vérifie si le language est sur le serveur.
            if lang in get_langs(server):
                await get_role_know(server, lang).delete()
                await get_role_learn(server, lang).delete()
                await context.channel.send(f'La langue **{lang}** vient d\'être supprimer !')
            else:
                await context.channel.send(f'La langue **{lang}** est inconnue.')
        else:
            await context.channel.send("Il manque le nom de la langue ou alors vous n'êtes pas modérateur.")

    @commands.command(pass_context=True)
    async def speakers(self, context, *args):
        """Afficher la liste des gens qui connaissent une certaine langue."""
        # Vérifie que la commande à au moins un argument
        if len(args) >= 1:
            server = context.message.guild
            lang = normalize(args[0])
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
        else:
            await context.channel.send("Il manque le nom de la langue.")

    @commands.command(pass_context=True)
    async def learners(self, context, *args):
        """Afficher la liste des gens qui apprennent une certaine langue."""
        # Vérifie que la commande à au moins un argument
        if len(args) >= 1:
            server = context.message.guild
            lang = normalize(args[0])
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
        else:
            await context.channel.send("Il manque le nom de la langue.")

    @commands.command(pass_context=True)
    async def langs(self, context):
        """Afficher la liste des langages du serveur."""
        languages = get_langs(context.message.guild)
        await context.channel.send(f'Le serveur gère les {len(languages)} langue(s) suivantes : {enum(languages)}')

    @commands.command(pass_context=True)
    async def ideols(self, context):
        """Afficher la liste des idéolinguistes du serveur."""
        server = context.message.guild
        role = discord.utils.get(server.roles, name='Idéolinguiste')
        ideols = sorted([user.name for user in server.members if (role in user.roles)])
        if len(ideols) == 0:
            await context.channel.send(f"Personne n'est **idéolinguiste**.")
        elif len(ideols) == 1:
            await context.channel.send(f"Une seule personne est **idéolinguiste**: `{ideols[0]}`.")
        else:
            await context.channel.send(f"Ces personnes sont **idéolinguiste**: {enum(ideols)}")

    @commands.command(pass_context=True)
    async def ideol(self, context):
        """Assigner le rôle idéolinguiste."""
        server = context.message.guild
        role = discord.utils.get(server.roles, name='Idéolinguiste')
        await context.message.author.add_roles(role)
        await context.channel.send('Tu es maintenant idéolinguiste.')

    @commands.command(pass_context=True)
    async def rmvideol(self, context):
        """Retirer le rôle idéolinguiste."""
        server = context.message.guild
        role = discord.utils.get(server.roles, name='Idéolinguiste')
        await context.message.author.remove_roles(role)
        await context.channel.send('Tu es maintenant idéolinguiste.')
