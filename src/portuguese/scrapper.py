"""Roteamento principal para processamento de dados 
dos Dicionários da Língua Portuguesa.
"""


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

from nltk.tokenize import SyllableTokenizer as st

warnings.filterwarnings("ignore", category=UserWarning)


class _Connection:

    def _get_container(url: str, word: str):
        """Promove a conexão com dicionários onlines."""
        resp = requests.get(url + word, headers=HEADERS)
        container = BeautifulSoup(resp.text, 'html.parser')

        if '<div class="found">' in str(container):
            redirect = next((r['href'] 
            for r in container.select("ul.resultados a") 
                if r.select_one("span.list-link").text == word), 
                container.select_one("ul.resultados a")['href'])

            container = BeautifulSoup(requests.get(
            f"{DEFAULT_URL}{redirect}", headers=HEADERS).text, 'html.parser')

        return container, resp


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
    def Portuguese(palavra: str):
        """Retorna as informações de uma palavra da Língua Portuguesa."""

        container, status = _Connection._get_container(PRINCIPAL_URL, palavra)

        name = container.find("h1", itemprop="name").get_text(strip=True).lower()
        cardmain = container.find("p", class_=re.compile(r"(^|\s)conjugacao|significado textonovo(\s|$)"))
        etymology = getattr(cardmain.find("span", class_="etim"), 'text', [])

        speech_complement = re.search(r'^.*?\.', container.find("p", itemprop="description").text).group(0)
        partofspeech = [ps.text for ps in cardmain.find_all("span", class_="cl")] or speech_complement
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
        additional = str(getattr(container.find("div", id='desamb'), 'text', '')).strip()
        if additional:
            meanings.append(additional.replace("[", "").replace("]", "."))

        titsection = container.find(lambda x: x.name == 'p' and x.get('class') == ['adicional'])
        syllables = next((l.text for l in titsection.find_all("b", limit=2) if '-' in l.text), '-'.join(st().tokenize(name)))
        animations = Animations.analogic_sinonimos(name, sinonimos[:10])
        final, analogic_animations = DICTIONARY(name, status, syllables, partofspeech, meanings, etymology, sinonimos, antonyms), animations
        if animations:
            return final, analogic_animations
                    
        return final

