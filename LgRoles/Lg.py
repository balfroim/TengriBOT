import discord
from discord.ext import commands
from Utils import Utils, Word


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
            data = LgData(context, args[0])
            await self.add_role('learn', data)

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
            data = LgData(context, args[0])
            await self.add_role('know', data)

    async def add_role(self, kw, data):
        """
            Factorisation for the command lgk and lgf
            Parameters:
                kw: keyword either 'know' or 'learn'. [Str]
                data: useful data for the Languages class. [LgData]
        """
        okw = 'learn' if kw == 'know' else 'know'
        # Check if the language is in the server
        if data.language in data.lgs_list:
            # Check if the author haven't already the role
            if data.lg_roles[kw] not in data.author.roles:
                # Check if the author have already the other role
                if data.lg_roles[okw] in data.author.roles:
                    await self.bot.say(f'Tu {Word.elision("ne", Word.conjugate[okw]["tu"])} '
                                       f'plus {data.lg_and_det}, '
                                       f'tu {Word.elision("le", Word.conjugate[kw]["tu"])} !')
                    await self.bot.remove_roles(data.author, data.lg_roles[okw])
                else:
                    await self.bot.say(f'Tu {Word.conjugate[kw]["tu"]} maintenant {data.lg_and_det} !')
                # Add the role
                await self.bot.add_roles(data.author, data.lg_roles[kw])
            else:
                await self.bot.say(f'Tu {Word.conjugate[kw]["tu"]} déjà {data.lg_and_det} !')
        else:
            await self.bot.say(f'Le serveur ne gère pas encore {data.lg_and_det}, désolé !')

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
            data = LgData(context, args[0])
            # Check if the language is in the server
            if data.language in data.lgs_list:
                hadRole = False
                for kw in ('know', 'learn'):
                    if data.lg_roles[kw] in data.author.roles:
                        await self.bot.remove_roles(data.author, data.lg_roles[kw])
                        await self.bot.say(f'Tu {Word.elision("ne", Word.conjugate[kw]["tu"])} plus {data.lg_and_det}.')
                        hadRole = True
                if not hadRole:
                    await self.bot.say(f'Tu ne connaissais ni apprenais {data.lg_and_det} déjà.')
            else:
                await self.bot.say(f'Le serveur ne gère pas encore {data.lg_and_det}, désolé !')

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
            data = LgData(context, args[0])
            # Check if the role already exists
            if data.language not in data.lgs_list:
                await self.bot.create_role(server=data.server, name=data.lg_roles_name['learn'])
                await self.bot.create_role(server=data.server, name=data.lg_roles_name['know'])
                await self.bot.say(f'Le serveur gère maintenant {data.lg_and_det} !')
            else:
                await self.bot.say(f'Le serveur gérais déjà {data.lg_and_det} !')

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
            data = LgData(context, args[0])
            # Check if the language is in the server
            if data.language in data.lgs_list:
                await self.bot.delete_role(server=data.server, role=data.lg_roles['learn'])
                await self.bot.delete_role(server=data.server, role=data.lg_roles['know'])
                await self.bot.say(f'Le serveur ne gère plus {data.lg_and_det} !')
            else:
                await self.bot.say(f'Le serveur ne gère pas encore {data.lg_and_det}, désolé !')

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
            data = LgData(context, args[0])
            # Check if the language is in the server
            if data.language in data.lgs_list:
                await self.display_speaker_list(data, 'know')
            else:
                await self.bot.say(f'Le serveur ne gère pas encore {data.lg_and_det}, désolé !')

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
            data = LgData(context, args[0])
            # Check if the language is in the server
            if data.language in data.lgs_list:
                await self.display_speaker_list(data, 'learn')
            else:
                await self.bot.say(f'Le serveur ne gère pas encore {data.lg_and_det}, désolé !')

    async def display_speaker_list(self, data, kw):
        """
            Factorisation for the command lgklist and lgflist
            Parameters:
                kw: keyword either 'know' or 'learn'. [Str]
                data: useful data for the Languages class. [LgData]
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
        await self.bot.say(message)

    @commands.command(pass_context=True)
    async def lglist(self, context):
        """
            List all the languages handle by the server.
            Parameters:
                context: the context in which the message is sent. [Message]
        """
        # The server in which the command was executed
        server = context.message.server
        # La liste des languages.
        lgs_list = sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Connaît")])
        message = f'Le serveur gère les {len(lgs_list)} langue(s) suivantes : '
        message += ', '.join(lgs_list[:-1]) + f' et {lgs_list[-1]}.'
        await self.bot.say(message)


class LgData:
    """
        Contains useful data for the Languages class
        Attributes:
            server: the server in which the command was executed. [Server]
            author: the user who executed the command. [Client]
            language: the name of the language (Normalized). [Str]
            lg_and_det: the language with its determinant. [Str]
            lgs_list: the language list. [List(str)]
            lg_roles_names: the roles "Connaît" and "Apprend" 's names. [Dict[Str]]
            lg_roles: the roles "Connaît" and "Apprend". [Dict[Role]]
    """
    def __init__(self, context, language):
        self.server = context.message.server
        self.author = context.message.author
        self.language = Word.normalize(language)
        self.lg_and_det = Word.elision('le', self.language.lower())
        self.lgs_list = sorted([r.name.split(" ")[1] for r in self.server.roles if r.name.startswith("Connaît")])
        self.lg_roles_name = {'know': f'Connaît {self.language}', 'learn': f'Apprend {self.language}'}
        self.lg_roles = {'know': discord.utils.get(self.server.roles, name=f'Connaît {self.language}'),
                         'learn': discord.utils.get(self.server.roles, name=f'Apprend {self.language}')}
