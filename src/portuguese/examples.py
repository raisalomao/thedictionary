import re
import requests
from unidecode import unidecode
from typing import LiteralString, List
from bs4 import BeautifulSoup, Tag

from itertools import islice 

class Examples:
    """Percorre banco de dados em busca de frases e autores a partir de uma palavra.
    """

    def __init__(self, source = str,
        language: LiteralString = str,
        ) -> None:
        self.language = language
        self.source = source


    @staticmethod
    def pensador(palavra: str):
        """Faz uma busca de frases na fonte `Pensador`.
        """
        headers = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'pt-BR'}
        try:
            contentResponse = requests.get(f"https://www.pensador.com/{unidecode(palavra).lower()}/", headers=headers)
            if contentResponse.status_code == 404:
                raise Exception("Sem exemplos disponíveis")

            read = BeautifulSoup(contentResponse.content, features='html.parser')
            sentence = read.find('div', id='phrasesList', class_='phrases-list').find_all('p', class_=re.compile(r'\bfrase\b|\bfr\b'))
            author = read.find_all('span', class_="author-name")

            sentences: List[str] = [frase.getText() for frase in sentence]
            authors: List[str] = [autor.getText() for autor in author]

            if all(palavra in s.lower() for s in sentences):
                examples = [{'sentence': s, 'author': f'- {a}'} for s, a in zip(sentences, authors)]
            else:
                dicioResponse = requests.get(f"https://www.dicio.com.br/{unidecode(palavra).lower()}/", headers=headers)
                if dicioResponse.status_code == 404:
                    raise Exception("Sem exemplos disponíveis")

                dicioExamples = BeautifulSoup(dicioResponse.content, features='html.parser')
                sentences: List[str] = []
                authors: List[str] = []
                getSentences = dicioExamples.find("div", class_="frases")
                if getSentences is not None:
                    for span in getSentences.find_all('span'):
                        sentences.append(str(span.get_text()).strip().replace(f"\n{span.find('em').get_text()}", "") 
                        if span.find('em') is not None else str(span.get_text()).strip())
                        authors.append(span.find('em').get_text() if span.find('em') is not None else '')

                    if not any(sentences):
                        sentences = [re.sub(r"\s*<em>.*</em>", "", s.get_text().strip().replace(f"{s.find('em').get_text().strip()}", "")) 
                        for s in getSentences.contents if isinstance(s, Tag)]
                        authors = [string.find('em').get_text(strip=True) for string in getSentences.contents if isinstance(string, Tag)]

                    examples = [{'sentence': s, 'author': a} for s, a in islice(zip(sentences, authors), 10)]
                else:
                    examples = "Sem exemplos disponíveis"
                    
            '''Retorna um número de 10 exemplos, facilmente customizável
            '''
            return examples[:10]
        except Exception as e:
            return str(e)


