import discord
from discord.ext import commands
from Utils import Utils

class Languages:
    """Commandes relatives aux langues"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def lgl(self, context, *args):
        """
            Ajoute le badge "Apprend"
            $lg learn <language>
        """
        if len(args) == 1:
            data = LgData(context, args[0])
            await self.add_role('learn', data)
        else:
            await self.bot.say(f'Il faut un seul argument, pas {nb_args}.')

    @commands.command(pass_context=True)
    async def lgk(self, context, *args):
        """
            Ajoute le badge "Connaît"
            $lgk <language>
        """
        if len(args) == 1:
            data = LgData(context, args[0])
            await self.add_role('know', data)
        else:
            await self.bot.say(f'Il faut un seul argument, pas {nb_args}.')

    async def add_role(self, kw, data):
        okw = 'learn' if kw == 'know' else 'know'
        kw_fr = 'apprends' if kw == 'learn' else 'connais'
        okw_fr = 'apprends' if okw == 'learn' else 'connais'
        # Check if the language is in the server
        if data.language in data.lgs_list:
            # Check if the author haven't already the learn role
            if data.lg_roles[kw] not in data.author.roles:
                # Check if the author have have already the know role
                if data.lg_roles[okw] in data.author.roles:
                    await self.bot.say(f'Tu ne/n\' {okw_fr} plus {data.lg_and_det}, tu l\'/le {kw_fr} !')
                    await self.bot.remove_roles(data.author, data.lg_roles[okw])
                else:
                    await self.bot.say(f'Tu {kw_fr} maintenant {data.lg_and_det} !')
                # Add the role
                await self.bot.add_roles(data.author, data.lg_roles['learn'])
            else:
                await self.bot.say(f'Tu {kw_fr} déjà {data.lg_and_det} !')
        else:
            await self.bot.say(f'Le serveur ne gère pas encore {data.lg_and_det}, désolé !')

    @commands.command(pass_context=True)
    async def lgf(self, context, *args):
        """
            Oublie une langue.
            $lgf <language>
        """
        if len(args) == 1:
            data = LgData(context, args[0])
            # Check if the language is in the server
            if data.language in data.lgs_list:
                # Remove the role
                if data.lg_roles['know'] in data.author.roles:
                    await self.bot.remove_roles(data.author, data.lg_roles['know'])
                    await self.bot.say(f'Tu ne connais plus {data.lg_and_det}.')
                elif data.lg_roles['learn'] in data.author.roles:
                    await self.bot.remove_roles(data.author, data.lg_roles['learn'])
                    await self.bot.say(f'Tu n\'apprend plus {data.lg_and_det}.')
                else:
                    await self.bot.say(f'Tu ne connaissais ni apprenais {data.lg_and_det} déjà.')
            else:
                await self.bot.say(f'Le serveur ne gère pas encore {data.lg_and_det}, désolé !')
        else:
            await self.bot.say(f'Il faut un seul argument, pas {nb_args}.')

    @commands.command(pass_context=True)
    async def lgadd(self, context, *args):
        """
            [MOD ONLY] Ajoute <language> au serveur.
            $lgadd <language>
        """
        data = LgData(context, args[0])
        if Utils.is_moderator(context, self.bot):
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
            [MOD ONLY] Retire <language> au serveur.
            $lgrmv <language>
        """
        data = LgData(context, args[0])
        if Utils.is_moderator(context, self.bot):
            # Check if the language is in the server
            if data.language in data.lgs_list:
                await self.bot.delete_role(data.server, name=data.lg_roles_name['learn'])
                await self.bot.delete_role(data.server, name=data.lg_roles_name['know'])
                await self.bot.say(f'Le serveur ne gère plus {data.lg_and_det} !')
            else:
                await self.bot.say(f'Le serveur ne gère pas encore {data.lg_and_det}, désolé !')

    @commands.command(pass_context=True)
    async def lgklist(self, context, *args):
        """
            Liste des gens qui connaisse ce <language>
            $lgklist <language>
        """
        # The server in which the command was executed
        server = context.message.server
        # The name of the language (Normalized)
        language = args[0][0].upper() + args[0][1:].lower() if len(args) == 1 else "NOT_SPECIFIED"
        # Language avec son determinant le ou l'
        lg_and_det = "l'" + language if language[0] in 'AEUIO' else "le " + language
        # La liste des languages.
        lgs_list = sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Connaît")])

        # Check if the language is in the server
        if language in lgs_list:
            know_role_name = "Connaît %s" % language
            know_role = discord.utils.get(server.roles, name=know_role_name)
            whoknow_list = sorted([user.name for user in server.members if (know_role in user.roles)])

            # Display the list
            if len(whoknow_list) > 1:
                message = f'{len(whoknow_list)} personnes connaissent {lg_and_det}: '
                for member in whoknow_list[:-2]:
                    message += member + ", "
                message += f"{whoknow_list[-2]} et {whoknow_list[-1]}."
            elif len(whoknow_list) == 1:
                message = f'Seul {whoknow_list[0]} connaît {lg_and_det}.'
            else:
                message = f'Personne ne connaît {lg_and_det}.'

            await self.bot.say(message)
        else:
            await self.bot.say(f'Le serveur ne gère pas encore {lg_and_det}, désolé !')
            return

    @commands.command(pass_context=True)
    async def lgllist(self, context, *args):
        """
            Liste des gens qui apprene ce <language>
            $lgllist <language>
        """
        # The server in which the command was executed
        server = context.message.server
        # The name of the language (Normalized)
        language = args[0][0].upper() + args[0][1:].lower() if len(args) == 1 else "NOT_SPECIFIED"
        # Language avec son determinant le ou l'
        lg_and_det = "l'" + language if language[0] in 'AEUIO' else "le " + language
        # La liste des languages.
        lgs_list = sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Apprend")])

        # Check if the language is in the server
        if language in lgs_list:
            learn_role_name = "Apprend %s" % language
            learn_role = discord.utils.get(server.roles, name=learn_role_name)
            wholearn_list = sorted([user.name for user in server.members if (learn_role in user.roles)])

            # Display the list
            if len(wholearn_list) > 1:
                message = f'{len(wholearn_list)} personnes apprend {lg_and_det}: '
                for member in wholearn_list[:-2]:
                    message += member + ", "
                message += f'{wholearn_list[-2]} et {wholearn_list[-1]}.'
            elif len(wholearn_list) == 1:
                message = f'Seul {wholearn_list[0]} apprend %s.'
            else:
                message = f'Personne n\'apprends {lg_and_det}.'

            await self.bot.say(message)
        else:
            await self.bot.say(f'Le serveur ne gère pas encore {lg_and_det}, désolé !')
            return

    @commands.command(pass_context=True)
    async def lglist(self, context):
        """
            Liste des languages du serveur.
            $lglist <language>
        """
        # The server in which the command was executed
        server = context.message.server
        # La liste des languages.
        lgs_list = sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Connaît")])

        message = f'Le serveur gère les {len(lgs_list)} langue(s) suivantes : '
        for language in lgs_list[:-2]:
            message += language + ', '
        message += f'{lgs_list[-2]} et {lgs_list[-1]}.'

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
            lg_roles: the roles "Connaît" and "Apprend". [Dict]
    """
    def __init__(self, context, language):
        self.server = context.message.server
        self.author = context.message.author
        self.language = language[0].upper() + language[1:].lower()
        self.lg_and_det = "l'" + language if language[0] in 'AEUIO' else "le " + language
        self.lgs_list = sorted([r.name.split(" ")[1] for r in self.server.roles if r.name.startswith("Connaît")])
        self.lg_roles_name = {'know': f'Connaît {language}', 'learn': f'Apprend {language}'}
        self.lg_roles = {'know': discord.utils.get(self.server.roles, name=f'Connaît {language}'),
                         'learn': discord.utils.get(self.server.roles, name=f'Apprend {language}')}
