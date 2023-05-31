from unidecode import unidecode
from portuguese.examples import Examples

PRINCIPAL_URL = "https://www.dicio.com.br/pesquisa.php?q="
BASE_URL = "https://www.dicio.com.br"
HEADERS = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'pt-BR'}

def image_url(name):
    pass
    
def DICTIONARY(name: str, response: any, syllables: str, partofspeech: list, meanings: list, etymology: str, sinonimos: list, antonyms: list):
    return {
        'status': response.status_code,
        'lanuguage': 'portuguese',
        'results': [
            {
                'word': name.lower(),
                'syllables': syllables,
                'gramaticalClass': partofspeech,
                'meanings': meanings,
                'etymology': etymology,
                'sinonimos': sinonimos,
                'antonyms': antonyms,
                'examples': Examples.pensador(name.lower())
            }
        ]
    }
