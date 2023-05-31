import re
import warnings
import requests
from portuguese.visuals import Visuals

from typing import List
from bs4 import BeautifulSoup
from collections import OrderedDict
from portuguese.constants import DICTIONARY, HEADERS, PRINCIPAL_URL, BASE_URL

from nltk.tokenize.sonority_sequencing import SyllableTokenizer

warnings.filterwarnings("ignore", category=UserWarning)

class BasicInformations:
    """Processa um conjunto de recursos básicos voltados à palavra requisitada. 
    Envolve significados, separação silábica, sinônimos, antônimos, etimologia, 
    classes gramaticais e escrita original padrão no idioma identificado.
    """

    def __init__(self, 
        source: str = None,
        language: str = None,
    ) -> None:
        self.language = language
        self.source = source


    @staticmethod
    def Portuguese(palavra = str):
        '''Retorna um `dict` com as informações de uma palavra da Língua Portuguesa.
        '''

        assert palavra is not None, "A palavra não pode ser nula."

        url = f"{PRINCIPAL_URL}{palavra.lower()}".replace(" ", "-")
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise ValueError("Verifique a ortografia")
                
        container = BeautifulSoup(response.content, features='html.parser')

        if 'Busca' in container.text:
            container = container.find("ul", class_='resultados').find('a')
            url = f"{BASE_URL}{container['href']}"
            container = BeautifulSoup(requests.get(url, headers=HEADERS).content, features='html.parser')

        name = container.find("h1", itemprop="name").get_text(strip=True)

        cardmain = container.find("p", class_=re.compile(r"(^|\s)conjugacao(\s|$)")) or container.find("p", class_=re.compile(r"significado"))
        etymology = cardmain.find("span", class_="etim").text if cardmain.find("span", class_="etim") else []
            
        partofspeech = [elem.text for elem in cardmain.find_all("span", class_="cl")] or container.find("p", itemprop="description", class_="significado").text
        if 'Ainda não temos' in partofspeech:
            partofspeech = "Sem classes gramaticais" 

        wrapsection = container.find_all("p", class_="adicional sinonimos")
        sinonimos = [sino.text for sino in wrapsection[0].find_all("a")] if wrapsection else []
        antonyms = [ant.text for ant in wrapsection[1].find_all("a")] if len(wrapsection) >= 2 else []
                    
        for span in cardmain.select('span.cl, span.etim'):
            span.extract()
        portdoubt = str(container.find("div", id='desamb').text.strip()).replace('\n', ' ') if container.find("div", id='desamb') else None
        meanings: List[str] = list(
        OrderedDict.fromkeys([span.text.replace("[", "").replace("]", ".") for span in cardmain.select('span') if not (span.get('class') and 'tag' in span.get('class'))])
        )
        if portdoubt is not None:     
            meanings.append(portdoubt)

        titsection = container.find(lambda x: x.name == 'p' and x.get('class') == ['adicional'])
        listsyllable = titsection.find_all("b") if len(titsection.find_all("b")) > 1 else []
        syllables = next((elemento.text for elemento in listsyllable if '-' in elemento.text), '-'.join(SyllableTokenizer().tokenize(name.lower())))
            
        Visuals.analogic_sinonimos(name.lower(), sinonimos[:10])
        return DICTIONARY(name, response, syllables, partofspeech, meanings, etymology, sinonimos, antonyms)

