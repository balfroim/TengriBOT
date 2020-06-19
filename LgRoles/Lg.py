import discord
from discord.ext import commands
from Utils import Utils, Word


async def add_role(kw, lang, context):
    """
        Add either a know or a learn role.
        Parameters:
            kw: keyword either 'know' or 'learn'. [Str]
            lang: the language
            data: useful data for the Languages class. [LgData]
    """
    opp_kw = 'learn' if kw == 'know' else 'know'

    lg_ut = LgUtility(context, lang)

    # Check if the language is in the server
    if lang in lg_ut.lgs_list:
        # Check if the author haven't already the role
        if lg_ut.lg_roles[kw] not in lg_ut.author.roles:
            # Check if the author have already the other role
            if lg_ut.lg_roles[opp_kw] in lg_ut.author.roles:
                await lg_ut.channel.send(f'Tu {Word.elision("ne", Word.conjugate[opp_kw]["tu"])} '
                                   f'plus {lg_ut.lg_and_det}, '
                                   f'tu {Word.elision("le", Word.conjugate[kw]["tu"])} !')
                await context.message.author.remove_roles(lg_ut.lg_roles[opp_kw])
            else:
                await lg_ut.channel.send(f'Tu {Word.conjugate[kw]["tu"]} maintenant {lg_ut.lg_and_det} !')
            # Add the role
            await context.message.author.add_roles(lg_ut.lg_roles[kw])
        else:
            await lg_ut.channel.send(f'Tu {Word.conjugate[kw]["tu"]} déjà {lg_ut.lg_and_det} !')
    else:
        await lg_ut.channel.send(f'Le serveur ne gère pas encore {lg_ut.lg_and_det}, désolé !')


def get_langs(server):
    return sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Connait")])


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
        # Check if the command has enough arguments
        if await Utils.enough_args(len(args), 1, self.bot):
            # data = LgData(context, args[0])
            await add_role('learn', args[0], context)

    @commands.command(pass_context=True)
    async def iknow(self, context, *args):
        """
            Se donner le rôle "Connait" pour une langue.
            Parameters:
                context: the context in which the message is sent. [Message]
                args[0]: language's name. [Str]
        """
        # Check if the command has enough arguments
        if await Utils.enough_args(len(args), 1, self.bot):
            await add_role('know', args[0], context)

    @commands.command(pass_context=True)
    async def forget(self, context, *args):
        """Oublier une certaines langue."""
        # Vérifie que la commande à au moins un argument
        if await Utils.enough_args(len(args), 1, self.bot):
            

        # Check if the command has enough arguments
        if await Utils.enough_args(len(args), 1, self.bot):
            lg_ut = LgUtility(context, args[0])
            # Check if the language is in the server
            if lg_ut.language in lg_ut.lgs_list:
                had_role = False
                for kw in ('know', 'learn'):
                    if lg_ut.lg_roles[kw] in lg_ut.author.roles:
                        await context.message.author.remove_roles(lg_ut.lg_roles[kw])
                        await lg_ut.channel.send(f'Tu {Word.elision("ne", Word.conjugate[kw]["tu"])} plus '
                                                 f'{lg_ut.lg_and_det}.')
                        had_role = True
                if not had_role:
                    await lg_ut.channel.send(f'Tu ne connaissais ni apprenais {lg_ut.lg_and_det} déjà.')
            else:
                await lg_ut.channel.send(f'Le serveur ne gère pas encore {lg_ut.lg_and_det}, désolé !')

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
                await discord.utils.get(server.roles, name=f'Apprend {lang}').delete()
                await discord.utils.get(server.roles, name=f'Connait {lang}').delete()
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
            role = discord.utils.get(server.roles, name=f'Connait {lang}')
            speakers = sorted([user.name for user in server.members if (role in user.roles)])
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
            role = discord.utils.get(server.roles, name=f'Apprend {lang}')
            learners = sorted([user.name for user in server.members if (role in user.roles)])
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
        message = f'Le serveur gère les {len(languages)} langue(s) suivantes : ' \
                  + ', '.join(languages[:-1]) \
                  + f' et {languages[-1]}.'
        await context.channel.send(message)
