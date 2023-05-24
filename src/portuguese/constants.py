from unidecode import unidecode
from examples import Examples
from typing import Dict

SANITIZE: Dict[str, str] = {

    'força': 'forca-3',
    'forças': 'forcas-2',
    'forcar': 'forcar-2',
    'caca': 'caca-2',
    'cacas': 'cacas-2',
    'mídia': 'midia-2',
    'mão' : 'mao-2',
    'iaô' : 'iao-2'
    
}
def image_url(name):
    if name.lower() in SANITIZE:
        return f"https://s.dicio.com.br/{SANITIZE[name.lower()]}.jpg"
    else:
        return f"https://s.dicio.com.br/{unidecode(name).lower()}.jpg"
    
def DICTIONARY(name: str, response, syllables, partOfSpeech, meanings, etymology, sinonimos, antonyms):
    return {
        'status': response.status_code,
        'hrefimg': image_url(name=name.lower()),
        'typeDict': 'Dicionário de Português',
        'results': [
            {
                'word': name.lower(),
                'syllables': syllables,
                'gramaticalClass': partOfSpeech,
                'meanings': meanings,
                'etymology': etymology,
                'sinonimos': sinonimos,
                'antonyms': antonyms,
                'examples': Examples.pensador(name.lower())
            }
        ]
    }
