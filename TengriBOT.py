import discord
from discord.ext import commands

# Init the bot
bot = commands.Bot(command_prefix='$', description='Hello !')


@bot.event
async def on_ready():
    print('Logged in as %s' % bot.user.name)


@bot.command(pass_context=True)
async def ideol(context, *args):
    # The server in which the command was executed
    server = context.message.server
    # The user who executed the command
    author = context.message.author
    ideol_role = discord.utils.get(server.roles, name='Idéolinguiste')

    if len(args) != 0 and args[0].lower() == 'list':
        ideol_list = sorted([user.name for user in server.members if (ideol_role in user.roles)])
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
    else:
        if not (ideol_role in author.roles):
            await bot.add_roles(author, ideol_role)
            await bot.say('Tu es maintenant idéolinguiste !')
        else:
            await bot.say('Tu étais déjà idéolinguiste !')


@bot.command()
async def meme(*args):
    """Throw some memes   """
    meme_name = args[0] if len(args) >= 1 else "list"
    meme_config = await load_memeconfig()
    if meme_name != 'list':
        if meme_name in meme_config:
            await bot.say(meme_config[meme_name]['url'])
        else:
            await bot.say(f'Le même ({meme_name}) est inconnu.')
    else:
        # Liste des mêmes
        message = '```Markdown\n'
        meme_names = sorted(meme_config.keys())
        for name in meme_names:
            message += f'* {name}: {meme_config[name]["desc"]}\n'
        message += '```'
        await bot.say(message)

async def load_memeconfig():
    """Load the meme config
    Return
    ------
    meme_config = the meme config (dictionnary)
    meme_config = {name: {'url':str, 'desc':desc}, ...}"""
    config = {}
    with open('meme_config.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            name = line.split(';')[0]
            desc = line.split(';')[1]
            url = line.split(';')[2][:-1]
            config[name] = {'desc': desc, 'url': url}

    return config

@bot.command()
async def ping():
    await bot.say("Pong")

"""
@bot.event
async def on_message(msg):
    if msg.content.lower() == 'qqn pe me metr ideolingwist svp ?':
        await bot.say('C\'est fait')
        ideol_role = discord.utils.get(msg.server, name='Idéolinguiste')
        await bot.add_roles(msg.author, ideol_role)
"""


@bot.command(pass_context=True)
async def lg(context, *args):
    """Commande relative au language
        Syntaxe: $lg <key_word> <language>
        Key words :
            know = Ajoute le badge "Connait"
            learn = Ajoute le badge "Apprends"
            forget = Retire les badges en lien avec la langue
            add = Ajoute la langue au serveur (MODERATOR ONLY)
            rmv = Retire la langue du serveur (MODERATOR ONLY)
            list =  La liste de langues
            help = Menu d'aide
        """
    # The server in which the command was executed
    server = context.message.server
    # The user who executed the command
    author = context.message.author
    # The key word (know, learn, ...) (in lower case)
    key_word = args[0].lower()
    # The name of the language (Normalized)
    language = args[1][0].upper() + args[1][1:].lower() if len(args) > 1 else "NOT_SPECIFIED"
    # Language avec son determinant le ou l'
    lg_and_det = "l'" + language if language[0] in 'AEUIO' else "le " + language
    # La liste des languages.
    lgs_list = sorted([r.name.split(" ")[1] for r in server.roles if r.name.startswith("Connaît")])

    know_role_name = "Connaît %s" % language
    learn_role_name = "Apprend %s" % language
    if not (key_word in ('help', 'list', 'add')):
        # Check if the language is in the server
        if language in lgs_list:
            know_role = discord.utils.get(server.roles, name=know_role_name)
            learn_role = discord.utils.get(server.roles, name=learn_role_name)
        else:
            await bot.say(f'Le serveur ne gère pas encore {lg_and_det}, désolé !')
            return
    # CONNAIT
    if key_word == 'know':
        if know_role in author.roles:
            await bot.say(f'Tu connaîs déjà {lg_and_det} !')
        else:
            if learn_role in author.roles:
                await bot.say(f'Bravo, tu as finis d\'apprendre {lg_and_det} !')
                await bot.remove_roles(author, learn_role)
            else:
                await bot.say(f'Tu connaîs maintenant {lg_and_det} !')
            await bot.add_roles(author, know_role)
    # APPREND
    elif key_word == 'learn':
        if learn_role in author.roles:
            await bot.say(f'Tu apprends déjà {lg_and_det} !')
        else:
            if know_role in author.roles:
                await bot.say(f'Tu ne connais plus {lg_and_det}, tu l\'apprends !')
                await bot.remove_roles(author, know_role)
            else:
                await bot.say(f'Tu apprends maintenant {lg_and_det} !')
            await bot.add_roles(author, learn_role)
    # OUBLIE
    elif key_word == 'forget':
        if know_role in author.roles:
            await bot.remove_roles(author, know_role)
            await bot.say(f'Tu ne connais plus {lg_and_det}.')
        elif learn_role in author.roles:
            await bot.remove_roles(author, learn_role)
            await bot.say(f'Tu n\'apprend plus {lg_and_det}.')
        else:
            await bot.say(f'Tu ne connaissais ni apprenais {lg_and_det} déjà.')
    # AJOUT
    elif key_word == "add":
        if discord.utils.get(server.roles, name='Modération') in author.roles:
            if not (language in lgs_list):
                await bot.create_role(server, name=know_role_name)
                await bot.create_role(server, name=learn_role_name)
                await bot.say(f'Le serveur gère maintenant {lg_and_det} !')
            else:
                await bot.say(f'Le serveur gérais déjà {lg_and_det} !')
        else:
            await bot.say('Seul les modérateurs peuvent utiliser cet commande')
    # RETIRER
    elif key_word == "rmv":
        if discord.utils.get(server.roles, name='Modération') in author.roles:
            await bot.delete_role(server, know_role)
            await bot.delete_role(server, learn_role)
            await bot.say(f'Le serveur ne gère plus {lg_and_det} !')
        else:
            await bot.say('Seul les modérateurs peuvent utiliser cet commande')
    # WHOKNOW
    elif key_word == "whoknow":
        whoknow_list = sorted([user.name for user in server.members if (know_role in user.roles)])
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
    # WHOLEARN
    elif key_word == "wholearn":
        wholearn_list = sorted([user.name for user in server.members if (learn_role in user.roles)])
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
    # LIST
    elif key_word == "list":
        message = f'Le serveur gère les {len(lgs_list)} langue(s) suivantes : '
        for language in lgs_list[:-2]:
            message += language + ', '
        message += f'{lgs_list[-2]} et {lgs_list[-1]}.'

        await bot.say(message)
    # HELP
    elif key_word == "help":
        help_message = '```Markdown\n'
        help_message += '# (HELP) Commande lg :\n'
        help_message += '-' * 22 + '\n'
        help_message += '$lg know <language>: Ajoute le badge "Connaît"\n'
        help_message += '$lg learn <language>: Ajoute le badge "Apprend"\n'
        help_message += '$lg forget <language>: Oublie <language>\n'
        help_message += '$lg add <language>: Ajoute <language> au serveur (MODERATOR ONLY)\n'
        help_message += '$lg rmv <language>: Retire <language> du serveur (MODERATOR ONLY)\n'
        help_message += '$lg list : Liste des langues gérer par le serveur'
        help_message += '```'
        await bot.say(help_message)
    else:
        await bot.say(f'Le serveur ne gère pas le mot-clé \'{key_word}\' ! Faites $lg help pour plus d\'informations.')

with open('token.txt', 'r') as config:
    token = config.readlines()[0].split(' ')[0]

bot.run(token)
