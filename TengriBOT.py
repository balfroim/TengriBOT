import discord
import os
from discord.ext import commands

# Init the bot
bot = commands.Bot(command_prefix='$', description='Hello !')

@bot.event
async def on_ready():
    print('Logged in as %s' % bot.user.name)
    # TODO : Say when the bot is connected in the chan



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
            message = 'Il y %d idéolinguistes sur ce serveur : ' % nb_ideol
            for ideolinguist in ideol_list[:-2]:
                message += '%s, ' % ideolinguist
            message += '%s et %s.' % (ideol_list[-2], ideol_list[-1])
            await bot.say(message)
        elif nb_ideol == 1:
            await bot.say('Le seul idéolinguiste du serveur est %s.' % ideol_list[0])
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
            await bot.say("Le même (%s) est inconnu." % meme_name)
    else:
        #Liste des mêmes
        message = '```Markdown\n'
        meme_names = sorted(meme_config.keys())
        for name in meme_names:
            message += '* %s: %s\n' % (name, meme_config[name]['desc'])
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
        if language in lgs_list:
            know_role = discord.utils.get(server.roles, name=know_role_name)
            learn_role = discord.utils.get(server.roles, name=learn_role_name)
        else:
            await bot.say("Le serveur ne gère pas encore %s, désolé !" % lg_and_det)
            return
    # CONNAIT
    if key_word == 'know':
        if know_role in author.roles:
            await bot.say("Tu connaîs déjà %s !" % lg_and_det)
        else:
            if learn_role in author.roles:
                await bot.say("Bravo, tu as finis d'apprendre %s !" % lg_and_det)
                await bot.remove_roles(author, learn_role)
            else:
                await bot.say("Tu connaîs maintenant %s !" % lg_and_det)
            await bot.add_roles(author, know_role)
    # APPREND
    elif key_word == 'learn':
        if learn_role in author.roles:
            await bot.say("Tu apprends déjà %s !" % lg_and_det)
        else:
            if know_role in author.roles:
                await bot.say("Tu ne connais plus %s, tu l'apprends !" % lg_and_det)
                await bot.remove_roles(author, know_role)
            else:
                await bot.say("Tu apprends maintenant %s !" % lg_and_det)
            await bot.add_roles(author, learn_role)
    # OUBLIE
    elif key_word == 'forget':
        if know_role in author.roles:
            await bot.remove_roles(author, know_role)
            await bot.say("Tu ne connais plus %s." % lg_and_det)
        elif learn_role in author.roles:
            await bot.remove_roles(author, learn_role)
            await bot.say("Tu n'apprend plus %s." % lg_and_det)
        else:
            await bot.say("Tu ne connaissais ni apprenais %s déjà." % lg_and_det)
    # AJOUT
    elif key_word == "add":
        if discord.utils.get(server.roles, name='Modération') in author.roles:
            if not (language in lgs_list):
                await bot.create_role(server, name=know_role_name)
                await bot.create_role(server, name=learn_role_name)
                await bot.say('Le serveur gère maintenant %s !' % lg_and_det)
            else:
                await bot.say('Le serveur gérais déjà %s !' % lg_and_det)
        else:
            await bot.say('Seul les modérateurs peuvent utiliser cet commande')
    # RETIRER
    elif key_word == "rmv":
        if discord.utils.get(server.roles, name='Modération') in author.roles:
            await bot.delete_role(server, know_role)
            await bot.delete_role(server, learn_role)
            await bot.say('Le serveur ne gère plus %s !' % lg_and_det)
        else:
            await bot.say('Seul les modérateurs peuvent utiliser cet commande')
    # WHOKNOW
    elif key_word == "whoknow":
        whoknow_list = sorted([user.name for user in server.members if (know_role in user.roles)])
        if len(whoknow_list) > 1:
            message = '%d personnes connaissent %s: ' % (len(whoknow_list), lg_and_det)
            for member in whoknow_list[:-2]:
                message += member + ", "
            message += "%s et %s." % (whoknow_list[-2], whoknow_list[-1])
        elif len(whoknow_list) == 1:
            message = 'Seul %s connaît %s.' % (whoknow_list[0], lg_and_det)
        else:
            message = 'Personne ne connaît %s.' % lg_and_det

        await bot.say(message)
    # WHOLEARN
    elif key_word == "wholearn":
        wholearn_list = sorted([user.name for user in server.members if (learn_role in user.roles)])
        if len(wholearn_list) > 1:
            message = '%d personnes apprend %s: ' % (len(wholearn_list), lg_and_det)
            for member in wholearn_list[:-2]:
                message += member + ", "
            message += "%s et %s." % (wholearn_list[-2], wholearn_list[-1])
        elif len(wholearn_list) == 1:
            message = 'Seul %s apprend %s.' % (wholearn_list[0], lg_and_det)
        else:
            message = 'Personne n\'apprends %s.' % lg_and_det

        await bot.say(message)
    # LIST
    elif key_word == "list":
        message = 'Le serveur gère les %d langues suivantes : ' % len(lgs_list)
        for language in lgs_list[:-2]:
            message += language + ", "
        message += "%s et %s." % (lgs_list[-2], lgs_list[-1])

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
        await bot.say("Le serveur ne gère pas le mot-clé '%s' ! Faites $lg help pour plus d'informations." % key_word)

with open('token.txt', 'r') as config:
    token = config.readlines()[0].split(' ')[0]

bot.run(token)
