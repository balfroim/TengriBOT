from discord.ext import commands
from LgRoles.Ideol import Ideol
from Meme.Meme import Meme
from LgRoles.Lg import Languages

# Notes: Ignore this module for now
# from Translation.Translation import Translation

# Init the bot
bot = commands.Bot(command_prefix='$', description='Bot pour le Discord Linguisticae.')


@bot.event
async def on_ready():
    print('Logged in as %s' % bot.user.name)


# Add all the commands
bot.add_cog(Ideol(bot))
bot.add_cog(Meme(bot))
bot.add_cog(Languages(bot))

# Read the token and run the bot
with open('token.txt', 'r') as token_file:
    token = token_file.readlines()[0].split(' ')[0]

bot.run(token)
