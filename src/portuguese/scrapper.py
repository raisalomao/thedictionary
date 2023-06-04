"""Roteamento principal para processamento de dados 
dos Dicionários da Língua Portuguesa.
"""


import re
import warnings
import requests 
from visuals.visuals import Animations

from typing import List
from bs4 import BeautifulSoup
from pathlib import Path
from PyPDF2 import PdfReader
from collections import OrderedDict
from portuguese.constants import (
    DICTIONARY, 
    HEADERS, 
    PRINCIPAL_URL, 
    DEFAULT_URL
    )

from nltk.tokenize import SyllableTokenizer as st, word_tokenize
import nltk

warnings.filterwarnings("ignore", category=UserWarning)


class _Connection:
    """Cria e se conecta a sessões online.
    """

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

class _FileSanitize:
    """Dicionários salvos em documentos digitais
    são processados para coleta de informações e correção 
    seguindo técnicas de Processamento de Linguagem Natural.
    """

    def _checkfile(folder = str, filename = str) -> bool:
        '''Checa se o arquivo já existe
        '''
        if not all(isinstance(param, str) 
            for param in (folder, filename)):
            raise ValueError('Parâmetros devem ser string.')
        
        filepath = Path(folder) / filename
        return filepath.exists()

    @classmethod
    def reading_documents(cls, folder: str, filename: str, key: str
    ) -> bool:
        """Este é um leitor de arquivos e separador de conteúdo
        desde que uma ``key`` = palavra seja fornecida,
        salvando em um arquivo .json, salvando o nome, gramática
        e significados de uma palavra.

        Documentos voltados à língua portuguesa terminam com `pt`.
        
            A inserção ocorre de forma manual a fim de preservar a 
        segurança e confiabilidade do contéudo armazenado.
        """

        if '_pt' not in filename:
            return False

        if _FileSanitize._checkfile(folder, filename):
            return False

        filepath = Path(f"./{folder}") / filename

        doc = PdfReader(filepath)
        all_text: List[str] = []

        for page in doc.pages:
            text = page.extract_text()
            all_text.append(text)
            extract_text = "\n".join(all_text)

        with open(f"./{folder}/database.txt", 'w', encoding='utf-8') as f:
            f.write(extract_text)

        return True
    
    @classmethod
    def correct_text(cls, filename: str):

        with open(f"./documents/{filename}", 'r', 
        encoding='utf-8') as file:
            text = file.read()

        words = word_tokenize(text, language='portuguese')
        corpus = nltk.corpus.words.words()

        corrected_words = []
        for word in words:
            if word.lower() not in corpus:
                corrected_word = word 
            else:
                corrected_word = word

            corrected_words.append(corrected_word)

        corrected_filename = filename.replace('.txt', '_corrected.txt')
        with open(corrected_filename, 'w', encoding='utf-8') as file:
            file.write(' '.join(corrected_words))

        return corrected_filename
    
class BasicInformations:
    """Processa um conjunto de recursos básicos voltados à palavra. 
    Envolve significados, separação silábica, sinônimos, antônimos, etimologia, 
    classes gramaticais e escrita original padrão no idioma identificado.
    """

    def __init__(self, 
        source: str = None,
        language: str = None,
        filename: str = None,
    ) -> None:
        self.language = language
        self.source = source
        self._filename = filename


    def language_detection(self):
        """Identifica o idioma da palavra"""
        pass

    def dictionary_source(self):
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
    

