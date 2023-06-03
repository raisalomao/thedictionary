from portuguese.examples import Examples

PRINCIPAL_URL = "https://www.dicio.com.br/pesquisa.php?q="
DEFAULT_URL = "https://www.dicio.com.br"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
    
def DICTIONARY(
    name: str, 
    response: int, 
    syllables: str, 
    partofspeech: list, 
    meanings: list, 
    etymology: str, 
    sinonimos: list, 
    antonyms: list
):
    return {
        'status': response.status_code,
        'language': 'portuguese',
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
