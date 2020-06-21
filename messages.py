VERB_FORGET = {'2PS': 'oublies'}
VERB_LEARN = {'2PS': 'apprends', '3PS': 'apprend', '3PP': 'apprennent'}
VERB_KNOW = {'2PS': 'connais', '3PS': 'connait', '3PP': 'connaissent'}
VERB_BE = {'2PS': 'es', '3PS': 'est', '3PP': 'sont'}

ROLE_KNOW = 'Connait {lang}'
ROLE_LEARN = 'Apprend {lang}'

LANG = 'la langue **{lang}**'
IDEOL = '**idéolinguiste**'

ROLES_CHANGE = 'Tu {role_verb[2PS]} {role}.'
ROLES_NOBODY = 'Il n\'y a personne qui {role_verb[3PS]} {role}'
ROLES_ONE = 'Une seule personne {role_verb[3PS]} {role} : `{person}`'
ROLES_MANY = '{nb} personnes {role_verb[3PP]} {role} : {persons}'

IDEOL_ADD = 'Tu es maintenant idéolinguiste.'
IDEOL_RMV = 'Tu n\'es plus idéolinguiste.'

LANG_UNKNOWN = 'La langue **{lang}** est inconnue.'
LANG_EXISTS = 'La langue **{lang}** est déjà connue.'
LANG_NEW = 'La langue **{lang}** vient d\'être ajouter !'
LANG_RMV = 'La langue **{lang}** vient d\'être supprimer !'
LANG_MISSING = 'Il manque le nom de la langue.'
LANG_LIST = 'Le serveur gère les {nb_lang} langue(s) suivantes : {langs}'

MODO_FORBIDDEN = 'Tu dois être modérateur pour utiliser cette commande'
