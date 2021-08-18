from discord import Intents
from discord.ext import commands

from Assignations import Assignations, De_assignations, Listes, Moderation, Source

# Notes: Ignore this module for now
# from Translation.Translation import Translation

intents = Intents.default()
intents.members = True

# Init the bot
bot = commands.Bot(command_prefix='$', description='Bot pour le Discord Linguisticae.', intents=intents)


@bot.event
async def on_ready():
    print('Logged in as %s' % bot.user.name)


@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandNotFound):
        await context.message.channel.send("Désolé, mais je ne connais pas cette commande.")
    else:
        raise error


# Add all the commands
bot.add_cog(Assignations(bot))
bot.add_cog(De_assignations(bot))
bot.add_cog(Listes(bot))
bot.add_cog(Moderation(bot))
bot.add_cog(Source(bot))

# Read the token and run the bot
with open('token.txt', 'r') as token_file:
    token = token_file.readlines()[0].split(' ')[0]

bot.run(token)
