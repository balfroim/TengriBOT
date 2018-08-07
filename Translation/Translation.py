from discord.ext import commands
from yandex import Translater
from Utils import Utils


class Translation:
    """
        Translation's command
        Attributes:
            bot: the bot's instance. [Bot]
            ts_key: the key of the translation API (Yandex). [str]
    """
    def __init__(self, bot):
        self.bot = bot
        # Get the key of the translation API (Yandex).
        with open('Translation/yandex.txt', 'r') as key_file:
            self.ts_key = key_file.readlines()[0]

    @commands.command(name='ts')
    async def translate(self, *args):
        """
            Translate from "language A" to "language B".
            Parameters:
                args[0]: "language A". [str]
                args[1]: "language B". [str]
                args[2:]: text to translate. [str]
        """
        # Check if the command has enough arguments
        if await Utils.enough_args(len(args), 3, self.bot):
            from_lg, to_lg = args[0], args[1]
            txt = ' '.join(args[2])
            # Do the translation
            translater = TTranslater(key=self.ts_key, text=txt, from_lang=from_lg, to_lang=to_lg)
            translation = translater.translate()
            await self.bot.say(translation)

    @commands.command()
    async def tslist(self):
        """
            List all the languages handle by the Yandex API.
        """
        # Instantiate a translater object
        ts = TTranslater(key=self.ts_key, from_lang='en', to_lang='fr')
        # Get a list of language codes and their ISO code, take only the languages handle by the Yandex API
        with open('Translation/lgcode.txt', 'r') as lgcode_file:
            lgISO = {sline[0]: sline[1].rstrip('\n') for sline in [line.split(',') for line in lgcode_file.readlines()]
                     if sline[0] in ts.valid_langs}
        # Relate language code to the language in a comprehensible way (not like this comment...)
        lgs_list = [f'({lgcode}) **{language}**' for lgcode, language in lgISO.items()]
        # Create the message to display
        message = f'L\'API de traduction gère les {len(lgs_list)} langue(s) suivantes : \n'
        message += ', '.join(lgs_list[:-1]) + f' et {lgs_list[-1]}'
        await self.bot.say(message)


class TTranslater(Translater):
    """
        Dirty overriding (à la baraki) of the Yandex Translater class because of an error in the base class.
        See Yandex's documentation to know what is each attributes. If it doesn't exists, then it's not my problem ;)
    """
    def __init__(self, key=None, text=None, from_lang=None, to_lang=None, hint=None, ui=None):
        self.valid_lang = ['az', 'sq', 'am', 'en', 'ar', 'hy', 'af', 'eu', 'ba', 'be', 'bn', 'my', 'bg', 'bs', 'cy',
                           'hu', 'vi', 'ht', 'gl', 'nl', 'mrj', 'el', 'ka', 'gu', 'da', 'he', 'yi', 'id', 'ga', 'it',
                           'is', 'es', 'kk', 'kn', 'ca', 'ky', 'zh', 'ko', 'xh', 'km', 'lo', 'la', 'lv', 'lt', 'lb',
                           'mg', 'ms', 'ml', 'mt', 'mk', 'mi', 'mr', 'mhr', 'mn', 'de', 'ne', 'no', 'pa', 'pap', 'fa',
                           'pl', 'pt', 'ro', 'ru', 'ceb', 'sr', 'si', 'sk', 'sl', 'sw', 'su', 'tg', 'th', 'tl', 'ta',
                           'tt', 'te', 'tr', 'udm', 'uz', 'uk', 'ur', 'fi', 'fr', 'hi', 'hr', 'cs', 'sv', 'gd', 'et',
                           'eo', 'jv', 'ja']

        self.valid_format = ['plain', 'html']
        self.valid_default_ui = ['ru', 'en', 'tr']

        self.default_ui = 'fr'

        if not ui:
            self.ui = self.default_ui
        self.hint = hint if hint is not None else list()
        self.base_url = 'https://translate.yandex.net/api/v1.5/tr.json/'
        self.key = key
        self.text = text
        self.from_lang = from_lang
        self.to_lang = to_lang

    @property
    def valid_langs(self):
        return self.valid_lang
