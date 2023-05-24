import re
import json
import random
import requests

from constants import SANITIZE, DICTIONARY
from flask import Flask
from flask_caching import Cache
from datetime import date
from typing import List, LiteralString
from bs4 import BeautifulSoup
from unidecode import unidecode
from collections import OrderedDict

from nltk.tokenize.sonority_sequencing import SyllableTokenizer

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

class BasicInformations:
    """Processa um conjunto de recursos básicos voltados à palavra requisitada. 
    Envolve significados, separação silábica, sinônimos, antônimos, etimologia, 
    classes gramaticais e escrita original padrão no idioma identificado.
    """

    def __init__(self, source = str,
        language: LiteralString = str,
    ) -> None:
        self.language = language
        self.source = source


    @staticmethod
    @cache.cached(timeout=3600)
    def Portuguese(palavra: LiteralString = str):
        '''Retorna um `dict` com as informações de uma palavra da Língua Portuguesa.
        '''

        headers = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'pt-BR'}
        url = f"https://www.dicio.com.br/{SANITIZE[palavra.lower()]}/" if palavra.lower() in SANITIZE else f"https://www.dicio.com.br/{unidecode(palavra).lower()}/"

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        if response.status_code != 200:
            raise ValueError("Verifique a ortografia")
              
        scrappy = BeautifulSoup(response.content, features='html.parser')
        name = scrappy.find("h1", itemprop="name").getText(strip=True)
        baseMeanings = scrappy.find("p", class_=re.compile(r"(^|\s)conjugacao(\s|$)")) or scrappy.find("p", class_=re.compile(r"significado"))
        etymology = baseMeanings.find("span", class_="etim").getText() if baseMeanings.find("span", class_="etim") else 'Sem etimologia disponível'
        
        partOfSpeech = [elem.getText() for elem in baseMeanings.find_all("span", class_="cl")] or scrappy.find("p", itemprop="description", class_="significado").text
        if 'Ainda não temos' in partOfSpeech:
            partOfSpeech = "Sem classes gramaticais" 

        getSinonimos = scrappy.find("p", class_="adicional sinonimos")
        sinonimos = [sino.getText() for sino in getSinonimos.find_all("a")] if getSinonimos is not None else 'Sem sinônimos disponíveis'

        getAntonyms = scrappy.find_all("p", class_="adicional sinonimos")
        antonyms = [ant.getText() for ant in getAntonyms[1].find_all("a")] if len(getAntonyms) >= 2 else 'Sem antônimos disponíveis'
                
        for span in baseMeanings.select('span.cl, span.etim'):
            span.extract()
        portDoubt = str(scrappy.find("div", id='desamb').get_text().strip()).replace('\n', ' ') if scrappy.find("div", id='desamb') else None
        meanings: List[str] = list(
            OrderedDict.fromkeys([span.get_text() for span in baseMeanings.select('span') if not (span.get('class') and 'tag' in span.get('class'))])
        )
        if portDoubt is not None:     
            meanings.append(portDoubt)

        fetchSyllable = scrappy.find(lambda x: x.name == 'p' and x.get('class') == ['adicional'])
        ListSyllable = fetchSyllable.find_all("b") if len(fetchSyllable.find_all("b")) > 1 else None
        try:
            syllables = next((elemento.get_text() for elemento in ListSyllable if '-' in elemento.get_text()), name.lower())
        except TypeError:
            syllables = '-'.join(SyllableTokenizer().tokenize(name.lower()))
            
        return DICTIONARY(name, response, syllables, partOfSpeech, meanings, etymology, sinonimos, antonyms)
    

    def establishConnection(palavra: str):
        return BasicInformations.Portuguese(palavra)

    @app.route('/portuguese/', methods=['GET'])
    def Palavradodia():
        '''Gera uma palavra para o dia
        '''
        with open("./data.txt", encoding="utf-8") as file:
            words = file.read().splitlines()
        random.seed(date.today().day)
        palavra_do_dia = random.choice(words)

        return json.dumps({
            
            'today': f'{palavra_do_dia.capitalize()}', 
            'info': BasicInformations.Portuguese(unidecode(palavra_do_dia)),                  
                            
        }, ensure_ascii=False), 200, {'Content-Type': 'application/json'}

    @app.route('/portuguese/<palavra>', methods=['GET'])
    def DictionaryGeral(palavra):
        '''Executa todo o conjunto de rotas na API
        '''    
        typeBody = {'Content-Type': 'application/json'}
        try:
            getResult = json.dumps(BasicInformations.establishConnection(palavra))
            return getResult, 200, typeBody
        
        except Exception as e:
            return json.dumps({'status' : 404, 'error': f"This word was not found or does not exist in the Portuguese Dictionary  {e}"}), typeBody
    
if __name__ == '__main__':
    app.run()