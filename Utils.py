import discord


class Utils:
    """Some useful static methods."""

    @staticmethod
    async def is_moderator(context, bot):
        """
            Check the author is a moderator.
            Parameters:
                context: the message's context. [Message]
                bot: the bot's instance. [Bot]
            Return:
                True if author is a moderator, False otherwise.
        """
        author = context.message.author
        server = context.message.server
        if discord.utils.get(server.roles, name='Modération') in author.roles:
            return True
        else:
            await bot.say('Seul les modérateurs peuvent utiliser cette commande !')
            return False

    @staticmethod
    async def enough_args(nb_args, min_args, bot):
        """
            Check the author is a moderator.
            Parameters:
                nb_args: the number of arguments. [int >= 0]
                min_args: the minimum of arguments. [int >= 0]
                bot: the bot's instance. [Bot]
            Return:
                True if author is a moderator, False otherwise.
        """
        if nb_args >= min_args:
            return True
        else:
            await bot.say(f'Il faut au moins {min_args} arguments, pas {nb_args}.')
            return False
