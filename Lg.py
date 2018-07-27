import discord
from discord.ext import commands

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
        # The server in which the command was executed
        server = context.message.server
        # The user who executed the command
        author = context.message.author
        # The name of the language (Normalized)
        language = args[0][0].upper() + args[0][1:].lower() if len(args) == 1 else "NOT_SPECIFIED"
        # Language avec son determinant le ou l'
        lg_and_det = "l'" + language if language[0] in 'AEUIO' else "le " + language
        # La liste des languages.
        lgs_list = sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Apprend")])

        know_role_name = "Connaît %s" % language
        learn_role_name = "Apprend %s" % language

        # Check if the language is in the server
        if language in lgs_list:
            know_role = discord.utils.get(server.roles, name=know_role_name)
            learn_role = discord.utils.get(server.roles, name=learn_role_name)
        else:
            await self.bot.say(f'Le serveur ne gère pas encore {lg_and_det}, désolé !')
            return

        # Add the role
        if learn_role in author.roles:
            await self.bot.say(f'Tu apprends déjà {lg_and_det} !')
        else:
            if know_role in author.roles:
                await self.bot.say(f'Tu ne connais plus {lg_and_det}, tu l\'apprends !')
                await self.bot.remove_roles(author, know_role)
            else:
                await self.bot.say(f'Tu apprends maintenant {lg_and_det} !')
            await self.bot.add_roles(author, learn_role)

    @commands.command(pass_context=True)
    async def lgk(self, context, *args):
        """
            Ajoute le badge "Connaît"
            $lgk <language>
        """
        # The server in which the command was executed
        server = context.message.server
        # The user who executed the command
        author = context.message.author
        # The name of the language (Normalized)
        language = args[0][0].upper() + args[0][1:].lower() if len(args) == 1 else "NOT_SPECIFIED"
        # Language avec son determinant le ou l'
        lg_and_det = "l'" + language if language[0] in 'AEUIO' else "le " + language
        # La liste des languages.
        lgs_list = sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Connaît")])

        know_role_name = "Connaît %s" % language
        learn_role_name = "Apprend %s" % language

        # Check if the language is in the server
        if language in lgs_list:
            know_role = discord.utils.get(server.roles, name=know_role_name)
            learn_role = discord.utils.get(server.roles, name=learn_role_name)
        else:
            await self.bot.say(f'Le serveur ne gère pas encore {lg_and_det}, désolé !')
            return

        # Add the role
        if know_role in author.roles:
            await self.bot.say(f'Tu connaîs déjà {lg_and_det} !')
        else:
            if learn_role in author.roles:
                await self.bot.say(f'Bravo, tu as finis d\'apprendre {lg_and_det} !')
                await self.bot.remove_roles(author, learn_role)
            else:
                await self.bot.say(f'Tu connaîs maintenant {lg_and_det} !')
            await self.bot.add_roles(author, know_role)

    @commands.command(pass_context=True)
    async def lgf(self, context, *args):
        """
            Oublie une langue.
            $lgf <language>
        """
        # The server in which the command was executed
        server = context.message.server
        # The user who executed the command
        author = context.message.author
        # The name of the language (Normalized)
        language = args[0][0].upper() + args[0][1:].lower() if len(args) == 1 else "NOT_SPECIFIED"
        # Language avec son determinant le ou l'
        lg_and_det = "l'" + language if language[0] in 'AEUIO' else "le " + language
        # La liste des languages.
        lgs_list = sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Connaît")])

        know_role_name = "Connaît %s" % language
        learn_role_name = "Apprend %s" % language

        # Check if the language is in the server
        if language in lgs_list:
            know_role = discord.utils.get(server.roles, name=know_role_name)
            learn_role = discord.utils.get(server.roles, name=learn_role_name)
        else:
            await self.bot.say(f'Le serveur ne gère pas encore {lg_and_det}, désolé !')
            return

        # Remove the role
        if know_role in author.roles:
            await self.bot.remove_roles(author, know_role)
            await self.bot.say(f'Tu ne connais plus {lg_and_det}.')
        elif learn_role in author.roles:
            await self.bot.remove_roles(author, learn_role)
            await self.bot.say(f'Tu n\'apprend plus {lg_and_det}.')
        else:
            await self.bot.say(f'Tu ne connaissais ni apprenais {lg_and_det} déjà.')

    @commands.command(pass_context=True)
    async def lgadd(self, context, *args):
        """
            [MOD ONLY] Ajoute <language> au serveur.
            $lgadd <language>
        """
        # The server in which the command was executed
        server = context.message.server
        # The user who executed the command
        author = context.message.author
        # The name of the language (Normalized)
        language = args[0][0].upper() + args[0][1:].lower() if len(args) == 1 else "NOT_SPECIFIED"
        # Language avec son determinant le ou l'
        lg_and_det = "l'" + language if language[0] in 'AEUIO' else "le " + language
        # La liste des languages.
        lgs_list = sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Connaît")])

        know_role_name = "Connaît %s" % language
        learn_role_name = "Apprend %s" % language

        # Create the role
        if discord.utils.get(server.roles, name='Modération') in author.roles:
            if language not in lgs_list:
                await self.bot.create_role(server=server, name=know_role_name)
                await self.bot.create_role(server=server, name=learn_role_name)
                await self.bot.say(f'Le serveur gère maintenant {lg_and_det} !')
            else:
                await self.bot.say(f'Le serveur gérais déjà {lg_and_det} !')
        else:
            await self.bot.say('Seul les modérateurs peuvent utiliser cet commande')

    @commands.command(pass_context=True)
    async def lgrmv(self, context, *args):
        """
            [MOD ONLY] Retire <language> au serveur.
            $lgrmv <language>
        """
        # The server in which the command was executed
        server = context.message.server
        # The user who executed the command
        author = context.message.author
        # The name of the language (Normalized)
        language = args[0][0].upper() + args[0][1:].lower() if len(args) == 1 else "NOT_SPECIFIED"
        # Language avec son determinant le ou l'
        lg_and_det = "l'" + language if language[0] in 'AEUIO' else "le " + language
        # La liste des languages.
        lgs_list = sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Connaît")])

        know_role_name = "Connaît %s" % language
        learn_role_name = "Apprend %s" % language

        # Check if the language is in the server
        if language in lgs_list:
            know_role = discord.utils.get(server.roles, name=know_role_name)
            learn_role = discord.utils.get(server.roles, name=learn_role_name)
        else:
            await self.bot.say(f'Le serveur ne gère pas encore {lg_and_det}, désolé !')
            return

        # Remove the role
        if discord.utils.get(server.roles, name='Modération') in author.roles:
            await self.bot.delete_role(server, know_role)
            await self.bot.delete_role(server, learn_role)
            await self.bot.say(f'Le serveur ne gère plus {lg_and_det} !')
        else:
            await self.bot.say('Seul les modérateurs peuvent utiliser cet commande')

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