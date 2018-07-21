import discord
from discord.ext import commands
import sqlite3
import sys

# Init the bot
bot = commands.Bot(command_prefix='$', description='Bot pour le Discord Linguisticae.')


@bot.event
async def on_ready():
    print('Logged in as %s' % bot.user.name)
    createMemeDb = """CREATE TABLE IF NOT EXISTS meme(name text,url text,desc text);"""
    with sqlite3.connect('meme.db') as conn:
        cursor = conn.cursor()
        cursor.execute(createMemeDb)
        conn.commit()


@bot.command(pass_context=True)
async def ideolist(context):
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
        await bot.say(message)
    elif nb_ideol == 1:
        await bot.say(f'Le seul idéolinguiste du serveur est {ideol_list[0]}.')
    else:
        await bot.say('Il n\'y as pas d\'idéolinguiste')


@bot.command(pass_context=True)
async def ideol(context):
    """Ajoute le badge ideolinguiste"""
    # The server in which the command was executed
    server = context.message.server
    # The user who executed the command
    author = context.message.author
    # The role of ideolinguist
    ideol_role = discord.utils.get(server.roles, name='Idéolinguiste')

    if not (ideol_role in author.roles):
        await bot.add_roles(author, ideol_role)
        await bot.say('Tu es maintenant idéolinguiste !')
    else:
        await bot.say('Tu étais déjà idéolinguiste !')


@bot.command(pass_context=True)
async def rmvideol(context):
    """Retire le badge ideolinguiste"""
    # The server in which the command was executed
    server = context.message.server
    # The user who executed the command
    author = context.message.author
    # The role of ideolinguist
    ideol_role = discord.utils.get(server.roles, name='Idéolinguiste')

    if ideol_role in author.roles:
        await bot.remove_roles(author, ideol_role)
        await bot.say('Tu n\'es plus idéolinguiste !')
    else:
        await bot.say('Tu n\'étais pas idéolinguiste !')


@bot.command()
async def meme(*args):
    """
        Affiche un meme
        $meme <name>
    """

    # check if it's the right length
    if len(args) == 1:
        name = args[0].lower()
    else:
        await bot.say(f'Il faut seulement 1 argument, pas {len(args)}.')
        return

    try:
        with sqlite3.connect('meme.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT url FROM meme WHERE name = ?;", (name,))
            url = cursor.fetchone()[0]
        await bot.say(url)
    except:
        await bot.say(f'Désolé il y a eu une erreur : {sys.exc_info()}')


@bot.command(pass_context = True)
async def memeadd(context, *args):
    """
        [MOD ONLY] Ajoute un même à la base de donnée
        $memeadd <name> <url> <desc>
    """
    author = context.message.author
    server = context.message.server
    # check if the author is a moderator
    isModerator = discord.utils.get(server.roles, name='Modération') in author.roles
    if not isModerator:
        await bot.say('Seul les modérateurs peuvent utiliser cette commande')
        return

    # check if it's the right length
    if len(args) >= 3:
        name = args[0].lower()
        url = args[1]
        desc = str()
        for word in args[2:-1]:
            desc += f'{word} '
        desc += args[-1]
    else:
        await bot.say(f'Il faut au moins 3 arguments, pas {len(args)}.')
        return

    try:
        with sqlite3.connect('meme.db') as conn:
            cursor = conn.cursor()
            # Check if the meme already exist
            cursor.execute("SELECT * FROM meme WHERE name = ?", (name,))
            if cursor.fetchone() is not None:
                await bot.say(f'Le meme "{name}" existe déjà')
                return
            # Create the meme in the database
            cursor.execute("INSERT INTO meme VALUES (?, ?, ?);", (name, url, desc))
            conn.commit()
        await bot.say(f'Le meme "{name}" a été ajouté avec l\'url : {url}')
    except:
        await bot.say(f'Désolé il y a eu une erreur : {sys.exc_info()}')


@bot.command(pass_context = True)
async def memermv(context, *args):
    """
        [MOD ONLY] Retire un même à la base de donnée
        $memermv <name>
    """
    author = context.message.author
    server = context.message.server
    # check if the author is a moderator
    isModerator = discord.utils.get(server.roles, name='Modération') in author.roles
    if not isModerator:
        await bot.say('Seul les modérateurs peuvent utiliser cette commande')
        return

    # check if it's the right length
    if len(args) == 1:
        name = args[0].lower()
    else:
        await bot.say(f'Il faut seulement 1 argument, pas {len(args)}.')
        return

    try:
        with sqlite3.connect('meme.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM meme WHERE name=?;", (name,))
            conn.commit()
        await bot.say(f'Le meme "{name}" a été supprimé.')
    except:
        await bot.say(f'Désolé il y a eu une erreur : {sys.exc_info()}')


@bot.command()
async def memelist():
    """Affiche la liste des mêmes"""
    try:
        with sqlite3.connect('meme.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, url, desc FROM meme;")
            mmlist = cursor.fetchall()
        if len(mmlist) == 0:
            await bot.say('Il n\'y a aucun même.')
        else:
            # Liste des mêmes
            message = '```Markdown\n'
            for mm in mmlist:
                name, desc = mm[0], mm[2]
                message += f'* {name}: {desc}\n'
            message += '```'
            await bot.say(message)
    except:
        await bot.say(f'Désolé il y a eu une erreur : {sys.exc_info()}')


@bot.command(pass_context=True)
async def lgl(context, *args):
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
        await bot.say(f'Le serveur ne gère pas encore {lg_and_det}, désolé !')
        return

    # Add the role
    if learn_role in author.roles:
        await bot.say(f'Tu apprends déjà {lg_and_det} !')
    else:
        if know_role in author.roles:
            await bot.say(f'Tu ne connais plus {lg_and_det}, tu l\'apprends !')
            await bot.remove_roles(author, know_role)
        else:
            await bot.say(f'Tu apprends maintenant {lg_and_det} !')
        await bot.add_roles(author, learn_role)


@bot.command(pass_context=True)
async def lgk(context, *args):
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
        await bot.say(f'Le serveur ne gère pas encore {lg_and_det}, désolé !')
        return

    # Add the role
    if know_role in author.roles:
        await bot.say(f'Tu connaîs déjà {lg_and_det} !')
    else:
        if learn_role in author.roles:
            await bot.say(f'Bravo, tu as finis d\'apprendre {lg_and_det} !')
            await bot.remove_roles(author, learn_role)
        else:
            await bot.say(f'Tu connaîs maintenant {lg_and_det} !')
        await bot.add_roles(author, know_role)


@bot.command(pass_context=True)
async def lgf(context, *args):
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
        await bot.say(f'Le serveur ne gère pas encore {lg_and_det}, désolé !')
        return

    # Remove the role
    if know_role in author.roles:
        await bot.remove_roles(author, know_role)
        await bot.say(f'Tu ne connais plus {lg_and_det}.')
    elif learn_role in author.roles:
        await bot.remove_roles(author, learn_role)
        await bot.say(f'Tu n\'apprend plus {lg_and_det}.')
    else:
        await bot.say(f'Tu ne connaissais ni apprenais {lg_and_det} déjà.')


@bot.command(pass_context=True)
async def lgadd(context, *args):
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
            await bot.create_role(server=server, name=know_role_name)
            await bot.create_role(server=server, name=learn_role_name)
            await bot.say(f'Le serveur gère maintenant {lg_and_det} !')
        else:
            await bot.say(f'Le serveur gérais déjà {lg_and_det} !')
    else:
        await bot.say('Seul les modérateurs peuvent utiliser cet commande')


@bot.command(pass_context=True)
async def lgrmv(context, *args):
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
        await bot.say(f'Le serveur ne gère pas encore {lg_and_det}, désolé !')
        return

    # Remove the role
    if discord.utils.get(server.roles, name='Modération') in author.roles:
        await bot.delete_role(server, know_role)
        await bot.delete_role(server, learn_role)
        await bot.say(f'Le serveur ne gère plus {lg_and_det} !')
    else:
        await bot.say('Seul les modérateurs peuvent utiliser cet commande')


@bot.command(pass_context=True)
async def lgklist(context, *args):
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

        await bot.say(message)
    else:
        await bot.say(f'Le serveur ne gère pas encore {lg_and_det}, désolé !')
        return


@bot.command(pass_context=True)
async def lgllist(context, *args):
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

        await bot.say(message)
    else:
        await bot.say(f'Le serveur ne gère pas encore {lg_and_det}, désolé !')
        return


@bot.command(pass_context=True)
async def lglist(context):
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

    await bot.say(message)

# Read the token and run the bot
with open('token.txt', 'r') as token_file:
    token = token_file.readlines()[0].split(' ')[0]

bot.run(token)
