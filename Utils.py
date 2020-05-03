import discord
import sqlite3

modo_rolenames = {"igidarúren «prophètes»", "díngen «divinités»", "Admin"}


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
        if not modo_rolenames.isdisjoint({role.name for role in author.roles}):
            return True
        else:
            await bot.say('Seul les modérateurs peuvent utiliser cette commande !')
            return False

    @staticmethod
    async def enough_args(nb_args, min_args, bot):
        """
            Check that the user give enough arguments.
            Parameters:
                nb_args: the number of arguments. [int >= 0]
                min_args: the minimum of arguments. [int >= 0]
                bot: the bot's instance. [Bot]
            Return:
                True if user give enough arguments.
        """
        if nb_args >= min_args:
            return True
        else:
            await bot.say(f'Il faut au moins {min_args} arguments, pas {nb_args}.')
            return False


class DatabaseCommunicator:
    """
        Use to communicate with a database.
        Attributes:
            db_path: path to the database file. (str)
            db_name: database's name. (str)
    """

    def __init__(self, db_path, db_name, column):
        """
            Constructor, create the database if not exists.
            Parameters:
                db_path: path to the database file. (str)
                db_name: database's name. (str)
                column: the database's column. (str) (ex: "name TEXT, age INT")
        """
        self.db_path = db_path
        self.db_name = db_name
        # Create the database if not exists
        createMemeDb = f"CREATE TABLE IF NOT EXISTS {self.db_name}({column});"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(createMemeDb)
            conn.commit()

    def select_w_cdt(self, column, condition):
        """
            Select all the rows that match the condition.
            Parameters:
                column: the column to return (after the SELECT). [str] (ex: '*' or 'name, desc, url')
                condition: the condition (after the WHERE). [str] (ex: 'name=meme')
            Return:
                result: all the rows that match the condition. [List(Tuple)]
        """
        #TODO: Make a better docstrings
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cdt_left, cdt_right = condition.split('=')
            cursor.execute(f"SELECT {column} FROM {self.db_name} WHERE {cdt_left} = ?;", (cdt_right,))
            result = cursor.fetchall()
        return result

    def select(self, column):
        """
            Select all the rows.
            Parameters:
                column: the column to return (after the SELECT). [str] (ex: '*' or 'name, desc, url')
            Return:
                result: all the rows that match the condition. [List(Tuple)]
        """
        #TODO: Make a better docstrings
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT {column} FROM {self.db_name}")
            result = cursor.fetchall()
        return result

    def insert(self, values):
        """
            Insert values into the database.
            Parameters:
                values: the values arranged in the columns order (after the VALUES). [Tuple]
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {self.db_name} VALUES (?, ?, ?);", values)
            conn.commit()

    def deletefrom(self, condition):
        """
            Delete rows from the database
            Parameters:
                condition: the condition to filter which rows to delete. [str]
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cdt_left, cdt_right = condition.split('=')
            cursor.execute(f"DELETE FROM {self.db_name} WHERE {cdt_left} = ?;", (cdt_right,))
            conn.commit()


class Word:
    """Use with word related function."""
    voyelles = 'aeiouAEIOU'
    # Dict use for quick conjugation
    conjugate = {'learn': {'tu': 'apprends', 'ils': 'apprennent', 'il': 'apprend'},
                 'know': {'tu': 'connais', 'ils': 'connaissent', 'il': 'connait'}}
    @staticmethod
    def normalize(word):
        """Normalize a word."""
        return word[0].upper() + word[1:].lower()

    @staticmethod
    def elision(word_before, word_after):
        """Make an elision if necessary. (https://fr.wikipedia.org/wiki/%C3%89lision)"""
        if word_before[-1] in Word.voyelles and word_after[0] in Word.voyelles:
            return f'{word_before[:-1]}\'{word_after}'
        else:
            return f'{word_before} {word_after}'

    @staticmethod
    def plural(amount, word):
        """Return the plural form of a word (if in plural)"""
        if word[-1] in 'szx' and amount <= 1:
            return word
        elif word.endwith('al'):
            # TODO: care about exceptions
            # (https://fr.wiktionary.org/wiki/Annexe:Pluriels_irr%C3%A9guliers_en_fran%C3%A7ais)
            return f'{word[:-2]}aux'
        else:
            return f'{word[-1]}s'