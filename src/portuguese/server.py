import re
import json
import random
import requests, nltk

from flask import Flask, request
from flask_caching import Cache
from datetime import date
from typing import List, LiteralString
from bs4 import BeautifulSoup
from unidecode import unidecode
from collections import OrderedDict
from constants import URL, SANITIZE, DICTIONARY

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
    @cache.cached(timeout=7200)
    def Portuguese(palavra: LiteralString = str):
        '''Retorna um `dict` com as informações de uma palavra da Língua Portuguesa.
        '''

        headers = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'pt-BR'}
        url = f"{URL}/{SANITIZE.get(palavra.lower(), unidecode(palavra).lower())}/".replace(" ", "-")

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ValueError("Verifique a ortografia")
              
        container = BeautifulSoup(response.content, features='html.parser')
        name = container.find("h1", itemprop="name").get_text(strip=True)
        cardmain = container.find("p", class_=re.compile(r"(^|\s)conjugacao(\s|$)")) or container.find("p", class_=re.compile(r"significado"))
        etymology = cardmain.find("span", class_="etim").text if cardmain.find("span", class_="etim") else 'Sem etimologia disponível'
        
        partofspeech = [elem.text for elem in cardmain.find_all("span", class_="cl")] or container.find("p", itemprop="description", class_="significado").text
        if 'Ainda não temos' in partofspeech:
            partofspeech = "Sem classes gramaticais" 

        wrapsection = container.find_all("p", class_="adicional sinonimos")
        sinonimos = [sino.text for sino in wrapsection[0].find_all("a")] if wrapsection else 'Sem sinônimos disponíveis'
        antonyms = [ant.text for ant in wrapsection[1].find_all("a")] if len(wrapsection) >= 2 else 'Sem antônimos disponíveis'
                
        for span in cardmain.select('span.cl, span.etim'):
            span.extract()
        portdoubt = str(container.find("div", id='desamb').text.strip()).replace('\n', ' ') if container.find("div", id='desamb') else None
        meanings: List[str] = list(
        OrderedDict.fromkeys([span.get_text() for span in cardmain.select('span') if not (span.get('class') and 'tag' in span.get('class'))])
        )
        if portdoubt is not None:     
            meanings.append(portdoubt)

        titsection = container.find(lambda x: x.name == 'p' and x.get('class') == ['adicional'])
        listsyllable = titsection.find_all("b") if len(titsection.find_all("b")) > 1 else []
        syllables = next((elemento.text for elemento in listsyllable if '-' in elemento.text), '-'.join(SyllableTokenizer().tokenize(name.lower())))
          
        return DICTIONARY(name, response, syllables, partofspeech, meanings, etymology, sinonimos, antonyms)
    

    def establishConnection(palavra: str):
        return BasicInformations.Portuguese(palavra)

    @app.route('/', methods=['GET'])
    def palavradodia():
        '''Gera uma palavra para o dia
        '''
        try:
            with open("./data.txt", encoding="utf-8") as file:
                words = file.read().splitlines()
            random.seed(date.today().day)
            palavra_do_dia = random.choice(words)

            return json.dumps({
                'today': f'{palavra_do_dia.capitalize()}', 
                'results': BasicInformations.Portuguese(unidecode(palavra_do_dia)),                                      
            }, ensure_ascii=False), 200, {'Content-Type': 'application/json'}
        
        except Exception:

            return '<p>\
            <span style="font-size: 30px;">Adicione uma palavra à URL<br><strong>Exemplo:</strong> \
            <a href="https://dicionario-solomon.onrender.com/palavra?format=json">\https://dicionario-solomon.onrender.com/palavra?format=json</a> \
            </span></p>', 404, {'Accept': 'text/plain'}

    @app.route('/<palavra>', methods=['GET'])
    def principal(palavra):
        '''Executa todo o conjunto de rotas na API
        '''    
        try:
            format_param = request.args.get('format', default='text')
            if format_param.lower() == 'json':
                getResult = json.dumps(BasicInformations.establishConnection(palavra))
                return getResult, 200, {'Content-Type': 'application/json; charset=utf-8'}
            else:
                getResult = BasicInformations.establishConnection(palavra)
                return str(getResult).encode('utf-8'), 200, {'Content-Type': 'text/plain; charset=utf-8'}
        
        except Exception as e:
            
            return json.dumps(
            {'status' : 404, 'error': f"This word was not found or does not exist in the Portuguese Dictionary {e}"},
            ensure_ascii=False), {'Content-Type': 'application/json; charset=utf-8'}
    
if __name__ == '__main__':
    nltk.download(['punkt'])
    app.run(debug=True)