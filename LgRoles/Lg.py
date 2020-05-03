import discord
from discord.ext import commands
from Utils import Utils, Word


async def display_speaker_list(context, data, kw):
    """
        Factorisation for the command lgklist and lgflist
        Parameters:
            kw: keyword either 'know' or 'learn'. [Str]
            data: useful data for the Languages class. [LgData]
            :param context:
    """
    speaker_list = sorted([user.name for user in data.server.members if (data.lg_roles[kw] in user.roles)])
    # Display the list
    if len(speaker_list) > 1:
        message = f'{len(speaker_list)} personnes {Word.conjugate[kw]["ils"]} {data.lg_and_det}: '
        message += ', '.join(speaker_list[:-1]) + f' et {speaker_list[-1]}.'
    elif len(speaker_list) == 1:
        message = f'Seul {speaker_list[0]} {Word.conjugate[kw]["il"]} {data.lg_and_det}.'
    else:
        message = f'Personne {Word.elision("ne", Word.conjugate[kw]["il"])} {data.lg_and_det}.'
    await context.channel.send(message)


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
            await context.message.author.add_roles(lg_ut.lg_roles[lg_ut.language])
        else:
            await lg_ut.channel.send(f'Tu {Word.conjugate[kw]["tu"]} déjà {lg_ut.lg_and_det} !')
    else:
        await lg_ut.channel.send(f'Le serveur ne gère pas encore {lg_ut.lg_and_det}, désolé !')


class Languages(commands.Cog):
    """
        Languages's command.
        Attributes:
            bot: the bot's instance. [Bot]
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def lgl(self, context, *args):
        """
            Add the role "Apprends" to the author.
            Parameters:
                context: the context in which the message is sent. [Message]
                args[0]: language's name. [Str]
        """
        # Check if the command has enough arguments
        if await Utils.enough_args(len(args), 1, self.bot):
            # data = LgData(context, args[0])
            await add_role('learn', args[0], context)

    @commands.command(pass_context=True)
    async def lgk(self, context, *args):
        """
            Add the role "Connaît" to the author.
            Parameters:
                context: the context in which the message is sent. [Message]
                args[0]: language's name. [Str]
        """
        # Check if the command has enough arguments
        if await Utils.enough_args(len(args), 1, self.bot):
            await add_role('know', args[0], context)

    @commands.command(pass_context=True)
    async def lgf(self, context, *args):
        """
            Remove roles "Connaît" or 'Apprend" to the author.
            Parameters:
                context: the context in which the message is sent. [Message]
                args[0]: language's name. [Str]
        """
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
    async def lgadd(self, context, *args):
        """
            [MOD ONLY] Add the language in the server.
            Parameters:
                context: the context in which the message is sent. [Message]
                args[0]: language's name. [Str]
        """
        # Check if the author is a moderator
        # Check if the command has enough arguments
        if await Utils.is_moderator(context, self.bot) and await Utils.enough_args(len(args), 1, self.bot):
            lg_ut = LgUtility(context, args[0])
            # Check if the role already exists
            if lg_ut.language not in lg_ut.lgs_list:
                #FIXME: Create role server level
                await self.bot.create_role(server=lg_ut.server, name=lg_ut.lg_roles_name['learn'])
                await self.bot.create_role(server=lg_ut.server, name=lg_ut.lg_roles_name['know'])
                await context.channel.send(f'Le serveur gère maintenant {lg_ut.lg_and_det} !')
            else:
                await context.channel.send(f'Le serveur gérais déjà {lg_ut.lg_and_det} !')

    @commands.command(pass_context=True)
    async def lgrmv(self, context, *args):
        """
            [MOD ONLY] Delete the language in the server.
            Parameters:
                context: the context in which the message is sent. [Message]
                args[0]: language's name. [Str]
        """
        # Check if the author is a moderator
        # Check if the command has enough arguments
        if await Utils.is_moderator(context, self.bot) and await Utils.enough_args(len(args), 1, self.bot):
            lg_ut = LgUtility(context, args[0])
            # Check if the language is in the server
            if lg_ut.language in lg_ut.lgs_list:
                # FIXME: Remove role server level
                await self.bot.delete_role(server=lg_ut.server, role=lg_ut.lg_roles['learn'])
                await self.bot.delete_role(server=lg_ut.server, role=lg_ut.lg_roles['know'])
                await context.channel.send(f'Le serveur ne gère plus {lg_ut.lg_and_det} !')
            else:
                await context.channel.send(f'Le serveur ne gère pas encore {lg_ut.lg_and_det}, désolé !')

    @commands.command(pass_context=True)
    async def lgklist(self, context, *args):
        """
            List all the people who know a language.
            Parameters:
                context: the context in which the message is sent. [Message]
                args[0]: language's name. [Str]
        """
        # Check if the command has enough arguments
        if await Utils.enough_args(len(args), 1, self.bot):
            lg_ut = LgUtility(context, args[0])
            # Check if the language is in the server
            if lg_ut.language in lg_ut.lgs_list:
                await display_speaker_list(context, lg_ut, 'know')
            else:
                await context.channel.send(f'Le serveur ne gère pas encore {lg_ut.lg_and_det}, désolé !')

    @commands.command(pass_context=True)
    async def lgllist(self, context, *args):
        """
            List all the people who learn a language.
            Parameters:
                context: the context in which the message is sent. [Message]
                args[0]: language's name. [Str]
        """
        # Check if the command has enough arguments
        if await Utils.enough_args(len(args), 1, self.bot):
            lg_ut = LgUtility(context, args[0])
            # Check if the language is in the server
            if lg_ut.language in lg_ut.lgs_list:
                await display_speaker_list(context, lg_ut, 'learn')
            else:
                await context.channel.send(f'Le serveur ne gère pas encore {lg_ut.lg_and_det}, désolé !')

    @commands.command(pass_context=True)
    async def lglist(self, context):
        """
            List all the languages handle by the server.
            Parameters:
                context: the context in which the message is sent. [Message]
        """
        # The server in which the command was executed
        server = context.message.guild
        # La liste des languages.
        lgs_list = sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Connaît")])
        message = f'Le serveur gère les {len(lgs_list)} langue(s) suivantes : '
        message += ', '.join(lgs_list[:-1]) + f' et {lgs_list[-1]}.'
        await context.channel.send(message)


class LgUtility:
    """
        Contains useful variable for method of the Lg class.
    """
    def __init__(self, context, language):
        self.channel = context.message.channel
        self.server = context.message.guild
        self.author = context.message.author
        self.language = Word.normalize(language)
        self.lg_and_det = Word.elision('le', self.language.lower())
        self.lgs_list = sorted([r.name.split(" ")[1] for r in self.server.roles if r.name.startswith("Connaît")])
        self.lg_roles_name = {'know': f'Connaît {self.language}', 'learn': f'Apprend {self.language}'}
        self.lg_roles = {'know': discord.utils.get(self.server.roles, name=f'Connaît {self.language}'),
                         'learn': discord.utils.get(self.server.roles, name=f'Apprend {self.language}')}
