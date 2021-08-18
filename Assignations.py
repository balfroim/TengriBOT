from textwrap import wrap

import discord
from discord.ext import commands

from messages import *


async def send_wrapped_message(channel, message):
    """Send a message in a channel (wrap it to be less than 2000 characters)."""
    for part in wrap(message, 2000):
        await channel.send(part)


def get_langs(server):
    return sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Connait")])


def get_role_learn(server, lang):
    return discord.utils.get(server.roles, name=f'Apprend {lang}')


def get_role_know(server, lang):
    return discord.utils.get(server.roles, name=f'Connait {lang}')


def ref_suggestion(server):
    return discord.utils.get(server.text_channels, name=f'suggestions🔧').mention


def enum(people):
    return f"`{'`, `'.join(people[:-1])}` et `{people[-1]}`"


def normalize(word):
    """Normalize a word."""
    return word[0].upper() + word[1:].lower()


def can_manage_roles(context):
    """Check if the author can manage roles."""
    channel = context.channel
    member = context.message.author
    return dict(channel.permissions_for(member))['manage_roles']


async def change_role(context, langs, verb, rmv_role_fcts, add_role_fcts):
    if len(langs) < 1:
        await context.channel.send(LANG_MISSING)
    else:
        server = context.message.guild
        for lang in langs:
            if lang not in get_langs(server):
                await context.channel.send(LANG_UNKNOWN.format(lang=lang, channel=ref_suggestion(server)))
            else:
                await context.message.author.remove_roles(*[rmv_role(server, lang) for rmv_role in rmv_role_fcts])
                await context.message.author.add_roles(*[add_role(server, lang) for add_role in add_role_fcts])
                await context.channel.send(ROLES_CHANGE.format(role_verb=verb, role=LANG.format(lang=lang)))

### ASSIGNATIONS

class Assignations(commands.Cog):
    """Commandes d'assignation"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ilearn(self, context, *args):
        """Assigner le rôle "Apprends" pour une langue."""
        langs = [normalize(lang) for lang in args]
        await change_role(context, langs, VERB_LEARN, [get_role_know], [get_role_learn])

    @commands.command(pass_context=True)
    async def ispeak(self, context, *args):
        """Assigner le rôle "Connait" pour une langue."""
        langs = [normalize(lang) for lang in args]
        await change_role(context, langs, VERB_KNOW, [get_role_learn], [get_role_know])

    @commands.command(pass_context=True)
    async def ideol(self, context):
        """Assigner le rôle idéolinguiste."""
        server = context.message.guild
        role = discord.utils.get(server.roles, name='Idéolinguiste')
        await context.message.author.add_roles(role)
        await context.channel.send(IDEOL_ADD)
        
### DE-ASSIGNATIONS

class De_assignations(commands.Cog):
    """Commandes de dé-assignation"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def forget(self, context, *args):
        """Oublier une certaine langue."""
        langs = [normalize(lang) for lang in args]
        await change_role(context, langs, VERB_FORGET, [get_role_learn, get_role_know], [])

    @commands.command(pass_context=True)
    async def rmvideol(self, context):
        """Retirer le rôle idéolinguiste."""
        server = context.message.guild
        role = discord.utils.get(server.roles, name='Idéolinguiste')
        await context.message.author.remove_roles(role)
        await context.channel.send(IDEOL_RMV)

### LISTES
        
class Listes(commands.Cog):
    """Commandes pour lister des informations"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def langs(self, context):
        """Afficher la liste des langages du serveur."""
        languages = get_langs(context.message.guild)
        await context.channel.send(LANG_LIST.format(nb_lang=len(languages), langs=enum(languages)))

    @commands.command(pass_context=True)
    async def learners(self, context, *args):
        """Afficher la liste des gens qui apprennent une certaine langue."""
        if len(args) < 1:
            await context.channel.send(LANG_MISSING)
        else:
            server = context.message.guild
            lang = normalize(args[0])
            members = server.fetch_members()
            learners = sorted([user.name async for user in members if (get_role_learn(server, lang) in user.roles)])
            if lang not in get_langs(server):
                await context.channel.send(LANG_UNKNOWN.format(lang=lang, channel=ref_suggestion(server)))
            elif len(learners) == 0:
                await context.channel.send(ROLES_NOBODY.format(role_verb=VERB_LEARN, role=LANG.format(lang=lang)))
            elif len(learners) == 1:
                await context.channel.send(ROLES_ONE.format(role_verb=VERB_LEARN, person=learners[0],
                                                            role=LANG.format(lang=lang)))
            else:
                await send_wrapped_message(context.channel,
                                           ROLES_MANY.format(role_verb=VERB_LEARN, persons=enum(learners),
                                                             role=LANG.format(lang=lang), nb=len(learners)))

    @commands.command(pass_context=True)
    async def speakers(self, context, *args):
        """Afficher la liste des gens qui connaissent une certaine langue."""
        if len(args) < 1:
            await context.channel.send(LANG_MISSING)
        else:
            server = context.message.guild
            lang = normalize(args[0])
            members = server.fetch_members()
            speakers = sorted([user.name async for user in members if (get_role_know(server, lang) in user.roles)])
            if lang not in get_langs(server):
                await context.channel.send(LANG_UNKNOWN.format(lang=lang, channel=ref_suggestion(server)))
            elif len(speakers) == 0:
                await context.channel.send(ROLES_NOBODY.format(role_verb=VERB_KNOW, role=LANG.format(lang=lang)))
            elif len(speakers) == 1:
                await context.channel.send(ROLES_ONE.format(role_verb=VERB_KNOW, person=speakers[0],
                                                            role=LANG.format(lang=lang)))
            else:
                await send_wrapped_message(context.channel,
                                           ROLES_MANY.format(role_verb=VERB_KNOW, persons=enum(speakers),
                                                             role=LANG.format(lang=lang), nb=len(speakers)))

    @commands.command(pass_context=True)
    async def ideols(self, context):
        """Afficher la liste des idéolinguistes du serveur."""
        server = context.message.guild
        role = discord.utils.get(server.roles, name='Idéolinguiste')
        ideols = sorted([user.name for user in server.members if (role in user.roles)])
        if len(ideols) == 0:
            await context.channel.send(ROLES_NOBODY.format(role_verb=VERB_BE, role=IDEOL))
        elif len(ideols) == 1:
            await context.channel.send(ROLES_ONE.format(role_verb=VERB_BE, person=ideols[0], role=IDEOL))
        else:
            await send_wrapped_message(context.channel,
                                       ROLES_MANY.format(role_verb=VERB_BE, persons=enum(ideols),
                                                         role=IDEOL, nb=len(ideols)))

### MODERATION

class Moderation(commands.Cog):
    """Commandes de modération des langues"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def newlang(self, context, *args):
        """[MOD ONLY] Ajouter une langue."""
        if not can_manage_roles(context):
            await context.channel.send(MODO_FORBIDDEN)
        elif len(args) < 1:
            await context.channel.send(LANG_MISSING)
        else:
            server = context.message.guild
            lang = normalize(args[0])
            if lang in get_langs(server):
                await context.channel.send(LANG_EXISTS.format(lang=lang))
            else:
                await server.create_role(name=ROLE_KNOW.format(lang=lang))
                await server.create_role(name=ROLE_LEARN.format(lang=lang))
                await context.channel.send(LANG_NEW.format(lang=lang))

    @commands.command(pass_context=True)
    async def rmvlang(self, context, *args):
        """[MOD ONLY] Supprimer une langue."""
        if not can_manage_roles(context):
            await context.channel.send(MODO_FORBIDDEN)
        elif len(args) < 1:
            await context.channel.send(LANG_MISSING)
        else:
            server = context.message.guild
            lang = normalize(args[0])
            if lang not in get_langs(server):
                await context.channel.send(LANG_UNKNOWN.format(lang=lang, channel=ref_suggestion(server)))
            else:
                await get_role_know(server, lang).delete()
                await get_role_learn(server, lang).delete()
                await context.channel.send(LANG_RMV.format(lang=lang))

### SOURCE

class Source(commands.Cog):
    """Lien du code source du bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def source(self, context):
        """Lien github vers le code source."""
        await context.channel.send("https://github.com/balfroim/TengriBOT")
