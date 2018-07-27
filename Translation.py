import discord
from discord.ext import commands
from yandex import Translater

class Translation:
    """Commandes relative à la traduction rapide"""
    def __init__(self, bot):
        self.bot = bot
        with open('yandex.txt', 'r') as key_file:
            self.ts_key = key_file.readlines()[0]

    @commands.command(name='ts')
    async def translate(self, *args):
        """
            Traduit dans language à l'autre. /!\ Utilisez les codes languages
            $translate <to> <text...>
        """
        if len(args) < 3:
            await self.bot.say(f'Il faut au moins 3 arguments, pas {len(args)}.')
            return
        from_lg = args[0]
        to_lg = args[1]
        txt = str()

        for word in args[2:-1]:
            txt += f'{word} '
        txt += args[-1]

        translater = TTranslater(key=self.ts_key, text=txt, from_lang=from_lg, to_lang=to_lg)
        translation = translater.translate()

        await self.bot.say(translation)

    @commands.command()
    async def tslist(self):
        """
            Listes des languages disponibles pour traduction
        """
        # Get the ISO code languages
        with open('lgcode.txt', 'r') as lgcode_file:
            lgISO = {sline[0]: sline[1].rstrip('\n') for sline in [line.split(',') for line in lgcode_file.readlines()]}
        # Instantiate a translater object
        ts = TTranslater(key=self.ts_key, from_lang='en', to_lang='fr')
        # Supported languages lists
        lgs_list = list()
        for lgcode in ts.get_valid_langs():
            if lgcode in lgISO:
                # Translate from english to french
                # ts.set_text(lgISO[lgcode])
                lgs_list.append( f'({lgcode}) **{lgISO[lgcode]}**' )

        message = f'L\'API de traduction gère les {len(lgs_list)} langue(s) suivantes : \n'
        for language in lgs_list[:-2]:
            message += language + ', '
        message += f'{lgs_list[-2]} et {lgs_list[-1]}.'

        await self.bot.say(message)

class TTranslater(Translater):
    # Overriding du init de Translater en mode baraki à cause d'une erreur dans le module de Yandex
    def __init__(self, key=None, text=None, from_lang=None, to_lang=None, hint=[], ui=None):
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

        if not ui: self.ui = self.default_ui
        self.hint = hint
        self.base_url = 'https://translate.yandex.net/api/v1.5/tr.json/'
        self.key = key
        self.text = text
        self.from_lang = from_lang
        self.to_lang = to_lang

    def get_valid_langs(self):
        return self.valid_lang