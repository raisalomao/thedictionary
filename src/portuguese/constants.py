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
    'mão': 'mao-2',
    'iaô': 'iao-2',
    'forró': 'forro-2',
    'chá': 'cha-2',
    'vovó': 'vovo-2',
    'cocô': 'coco-3',
    'côcô': 'coco-3',
    'cocós': 'cocos-3',
    'cocó': 'coco-2',
    'chalé': 'chale-2',
    'fé': 'fe-2',
    'fê': 'fe-3',
    'fe': 'fe-3',
    'axé': 'axe-2',
    'rã': 'ra-2',
    'fubá': 'fuba-2',
    'felá': 'fela-2',
    'sabiá': 'sabia-2',
    'trará': 'trara-2',
    'dá': 'da-3',
    'dã': 'da-2',
    'sabá': 'saba-2',
    'ceará': 'ceara-2',
    'diva': 'diva-2',
    'quartã': 'quarta-2',
    'cristã': 'crista-2',
    'cã': 'ca-4',
    'ca': 'ca-2',
    'resedá': 'reseda-2',
    'virá': 'vira-2',
    'retrô': 'retro-2',
    'vô': 'vo-2',
    'vós': 'vos-2',
    'avô': 'avo-3',
    'faraó': 'farao-2',
    'japá': 'japa-2',
    'japás': 'japas-2',
    'jogó': 'jogo-2',
    'avós': 'avos-2',
    'cabrobó': 'cabrobo-2',
    'pato': 'pato-2',
    'domino': 'domino-3',
    'efó': 'efo-2',
    'caxingó': 'caxingo-2',
    'cipó': 'cipo-2',
    'coió': 'coio-2',
    'potó': 'poto-2',
    'pató': 'pato-2',
    'pió': 'pio-2',
    'piós': 'pios-2',
    'cotó': 'coto-2',
    'filós': 'filos-3'
    
}

URL = "https://www.dicio.com.br"

def image_url(name):
    if name.lower() in SANITIZE:
        return f"https://s.dicio.com.br/{SANITIZE[name.lower()]}.jpg"
    else:
        return f"https://s.dicio.com.br/{unidecode(name).lower()}.jpg"
    
def DICTIONARY(name: str, response, syllables, partOfSpeech, meanings, etymology, sinonimos, antonyms):
    return {
        'status': response.status_code,
        'lanuguage': 'portuguese',
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
