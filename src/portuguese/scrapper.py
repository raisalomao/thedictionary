import re
import warnings
import requests 
from visuals.visuals import Animations

from typing import List
from bs4 import BeautifulSoup
from collections import OrderedDict
from portuguese.constants import (
    DICTIONARY, 
    HEADERS, 
    PRINCIPAL_URL, 
    DEFAULT_URL
    )

from nltk.tokenize import SyllableTokenizer

warnings.filterwarnings("ignore", category=UserWarning)

class _Connection:

    def _get_container(url, word):
        """Promove a conexão com dicionários onlines."""
        resp = requests.Session().get(url + word, headers=HEADERS)
        return BeautifulSoup(resp.text, features='html.parser'), resp


class BasicInformations:
    """Processa um conjunto de recursos básicos voltados à palavra. 
    Envolve significados, separação silábica, sinônimos, antônimos, etimologia, 
    classes gramaticais e escrita original padrão no idioma identificado.
    """

    def __init__(self, 
        source: str = None,
        language: str = None,
    ) -> None:
        self.language = language
        self.source = source


    def language_detection():
        """Identifica o idioma da palavra"""
        pass

    def dictionary_source():
        """Direciona o endereço dos dicionários online"""
        pass


    @staticmethod
    def Portuguese(palavra = str):
        """Retorna as informações de uma palavra da Língua Portuguesa."""

        container, status = _Connection._get_container(PRINCIPAL_URL, palavra)

        if '<div class="found">' in str(container):
            otherway = container.find("ul", class_='resultados').find('a')
            container = BeautifulSoup(requests.Session().get(f"{DEFAULT_URL}{otherway['href']}", 
            headers=HEADERS).text, features='html.parser')

        name = container.find("h1", itemprop="name").get_text(strip=True).lower()
        cardmain = container.find("p", class_=re.compile(r"(^|\s)conjugacao|significado textonovo(\s|$)"))
        etymology = getattr(cardmain.find("span", class_="etim"), 'text', [])

        partofspeech = [ps.text for ps in cardmain.find_all("span", class_="cl")] or container.find("p", itemprop="description").text
        if 'Ainda não temos' in partofspeech:
            partofspeech = "Sem classes gramaticais" 

        wrapsection = container.find_all("p", class_="adicional sinonimos", limit=2)
        sinonimos = [sino.text for sino in wrapsection[0].find_all("a")] if wrapsection else []
        antonyms  = [ant.text for ant in wrapsection[1].find_all("a")] if len(wrapsection) >= 2 else []
                    
        for span in cardmain.select('span.cl, span.etim'):
            span.extract()
        meanings: List[str] = list(
        OrderedDict.fromkeys([span.text.replace("[", "").replace("]", ".") 
        for span in cardmain.select('span') if not (span.get('class') and 'tag' in span.get('class'))]))
        additional = str(getattr(container.find("div", id='desamb'), 'text', '')).strip().replace('\n', ' ')
        if additional:
            meanings.append(additional)

        titsection = container.find(lambda x: x.name == 'p' and x.get('class') == ['adicional'])
        syllables = next((l.text for l in titsection.find_all("b", limit=2) if '-' in l.text), '-'.join(SyllableTokenizer().tokenize(name)))
        animations = Animations.analogic_sinonimos(name, sinonimos[:10])
        final, analogic_animations = DICTIONARY(name, status, syllables, partofspeech, meanings, etymology, sinonimos, antonyms), animations
        if animations:
            return final, analogic_animations
                    
        return final

