from unidecode import unidecode
from examples import Examples
from typing import Dict

SANITIZE: Dict[str, str] = {

    'palavras': 'palavras',
    
}

URL = "https://www.dicionário.solomon.net"

def image_url(name):
    if name.lower() in SANITIZE:
        return f"https://solomonimg.com/{SANITIZE[name.lower()]}.jpg"
    else:
        return f"https://solomonimg.com/{unidecode(name).lower()}.jpg"
    
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
