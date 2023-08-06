import re
import unicodedata

from pynyol.dictanum import IntParser

""""
DISCLAIMER: most of this script is inspired or directly copied from other sources, such as github repos: 
- coqui-ai/TTS/TTS/tts/utils/text/cleaners.py
- Platchaa/VITS-fast-fine-tuning/text/english.py 
- jaywalnut310/vits/text/cleaners.py 
"""

_ABBREVIATIONS = [
    (re.compile("\\b%s\\b(\.*)" % x[0], re.IGNORECASE), x[1])
    for x in [
        ("srita", "señorita"),
        ("srito", "señorito"),
        ("sres", "señores"),
        ("sra", "señora"),
        ("sr", "señor"),
        ("dr", "doctor"),
        ("drs", "doctores")
    ]
]
    
_SYMBOLS = [
    (r";|:", ","),
    (r"'|´|`", "\""),
    (r"(\w)-(\w)", "\\1 \\2"), #numeric reference on replace needs backslash scaping or else it treats as a unicode
    (r"-", "—"),
    #this can not be "detected" as accents and replaced with normalization, maybe find another way, else keep them in symbols but add this to docs
    (r"ł", "l"), #l with stroke
    (r"ø", "o"), #o with stroke
    (r"ã", "a"), #a with tilde
    (r"ã", "a"), #a and tilde
    (r"õ", "o"), #o with tilde
    (r"õ", "o")  #o and tilde
    (r"ñ", "ñ")  #n and tilde
]

_KEEP_THIS_ACCENTS = "áéíóú"

_WHITESPACE_RE = re.compile('\s+')
_DOTTED_NUMBER_RE = re.compile(r'([0-9][0-9\.]+[0-9])')
_DECIMAL_NUMBER_RE = re.compile(r'([0-9]+\,[0-9]+)')
_EURO_RE = re.compile(r'£([0-9\,]*[0-9]+)')
_PESO_RE = re.compile(r'\$([0-9\.\,]*[0-9]+)')
_NUMBER_RE = re.compile(r'[0-9]+')

def expand_abbreviations(text, abbrev = None):
    if abbrev is None:
        abbrev = _ABBREVIATIONS

    for regex, replacement in abbrev:
        text = re.sub(regex, replacement, text)
    return text


def lowercase(text):
    return text.lower()


def collapse_whitespace(text):
    return re.sub(_WHITESPACE_RE, " ", text).strip()


def replace_symbols(text, symb = None):
    if symb is None:
        symb = _SYMBOLS

    for regex, replacement in symb:
        text = re.sub(regex, replacement, text)
    return text


def replace_accents(text, keep_this_accents = None):
    if keep_this_accents is None:
        keep_this_accents = _KEEP_THIS_ACCENTS
    
    return ''.join(unicodedata.normalize('NFKD', l) if l not in keep_this_accents else l for l in text)


def _remove_numeric_dots_callback(m):
    return m.group(1).replace('.', '')


def remove_numeric_dots(text):
    return re.sub(_DOTTED_NUMBER_RE, _remove_numeric_dots_callback, text)


def _expand_decimal_comma_callback(m):
    return m.group(1).replace(',', ' coma ')


def expand_decimal_comma(text):
    return re.sub(_DECIMAL_NUMBER_RE, _expand_decimal_comma_callback, text)


def _expand_pesos_callback(m):
    match = m.group(1)
    if '.' in match:
        parts = match.split('.')
    elif ',' in match:
        parts = match.split(',')
    else:
        parts = [match, '0']
    if len(parts) > 2:
        return match + ' pesos'  # Unexpected format
    pesos = int(parts[0]) if parts[0] else 0
    cents = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    if pesos and cents:
        peso_unit = 'peso' if pesos == 1 else 'pesos'
        cent_unit = 'centavo' if cents == 1 else 'centavos'
        return '%s %s con %s %s' % (pesos, peso_unit, cents, cent_unit)
    elif pesos:
        peso_unit = 'peso' if pesos == 1 else 'pesos'
        return '%s %s' % (pesos, peso_unit)
    elif cents:
        cent_unit = 'centavo' if cents == 1 else 'centavos'
        return '%s %s' % (cents, cent_unit)
    else:
        return 'cero pesos'


def expand_pesos(text):
    return re.sub(_PESO_RE, _expand_pesos_callback, text)


def _expand_euros_callback(m):
    match = m.group(1)
    if '.' in match:
        parts = match.split('.')
    elif ',' in match:
        parts = match.split(',')
    else:
        parts = [match, '0']
    if len(parts) > 2:
        return match + ' euros'  # Unexpected format
    euros = int(parts[0]) if parts[0] else 0
    cents = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    if euros and cents:
        euro_unit = 'euro' if euros == 1 else 'euros'
        cent_unit = 'centavo' if cents == 1 else 'centavos'
        return '%s %s con %s %s' % (euros, euro_unit, cents, cent_unit)
    elif euros:
        euro_unit = 'euro' if euros == 1 else 'euros'
        return '%s %s' % (euros, euro_unit)
    elif cents:
        cent_unit = 'centavo' if cents == 1 else 'centavos'
        return '%s %s' % (cents, cent_unit)
    else:
        return 'cero euros'


def expand_euros(text):
    return re.sub(_EURO_RE, _expand_euros_callback, text)


def _expand_number_callback(m):
    match = m.group(0)
    ip = IntParser(int(match.strip()))
    return ip.txt


def expand_number(text):
    return re.sub(_NUMBER_RE, _expand_number_callback, text)


def normalize_numbers(text):
    """
    Common use of numeric processing to text, for a more customized version, run each function separately
    """
    text = remove_numeric_dots(text)
    text = expand_euros(text)
    text = expand_pesos(text)
    text = expand_decimal_comma(text)
    text = expand_number(text)
    return text


def clean(text, clean_abbrev = True, abbrev = None, clean_symb = True, symb = None, clean_accents = True, keep_this_accents = None):
    """
    A simple example implementation of all functions above, with some customization, for better use create your own cleaning function using them separately.
    """

    text = lowercase(text)
    if clean_abbrev:
        text = expand_abbreviations(text, abbrev=abbrev)
    if clean_symb:
        text = replace_symbols(text, symb=symb)
    if clean_accents:
        text = replace_accents(text, keep_this_accents=keep_this_accents)
    text = normalize_numbers(text)
    text = collapse_whitespace(text)

    return text
    

