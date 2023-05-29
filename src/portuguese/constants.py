from unidecode import unidecode
from examples import Examples
from typing import Dict

SANITIZE: Dict[str, str] = {

    'palavras': 'palavras',
    
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
