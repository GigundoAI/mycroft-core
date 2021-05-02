"""
The mycroft.util.lang module provides the main interface for setting up the
lingua-franca (https://github.com/mycroftai/lingua-franca) selected language
"""

# we want to support both LF and LN
# when using the mycroft wrappers this is not an issue, but skills might use
# either, so mycroft-lib needs to account for this and set the defaults for
# both libs.

# lingua_franca/lingua_nostra are optional and might not be installed
# if needed provide dummy methods
# exceptions should only be raised in the parse and format utils

# TODO improve this, duplicating code is usually bad, consider
#  supporting only LN and making it a hard requirement, in this case
#  only skills importing LF would need to worry, the setter methods
#  should always account for both libs

try:
    import lingua_franca as LF
except ImportError:
    LF = None

try:
    import lingua_nostra as LN
except ImportError:
    LN = None

_lang = "en-us"


def get_primary_lang_code():
    if LN:
        return LN.get_primary_lang_code()
    if LF:
        return LF.get_primary_lang_code()
    return _lang.split("-")[0]


def get_default_lang():
    if LN:
        return LN.get_default_lang()
    if LF:
        return LF.get_default_lang()
    return _lang


def set_default_lang(lang):
    global _lang
    _lang = lang
    if LN:
        LN.set_default_lang(lang)
    if LF:
        LF.set_default_lang(lang)


def load_languages(langs):
    if LN:
        LN.load_languages(langs)
    if LF:
        LF.load_languages(langs)


def load_language(lang):
    if LN:
        LN.load_language(lang)
    if LF:
        LF.load_language(lang)
