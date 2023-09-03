import re
import requests
from typing import LiteralString, List
from bs4 import BeautifulSoup, Tag

from itertools import islice 

class Examples:
    """Percorre banco de dados em busca de sentenças e 
    autores a partir de uma palavra.
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
            pensador_resp = requests.get(f"https://www.pensador.com/busca.php?q={palavra.lower()}", headers=headers)

            read = BeautifulSoup(pensador_resp.text, features='html.parser')
            sentence = read.find('div', class_='phrases-list').find_all('p', class_=re.compile(r'\bfrase\b|\bfr\b'))
            author = read.find_all('span', class_="author-name")

            sentences: List[str] = [frase.text for frase in sentence]
            authors: List[str] = [autor.text for autor in author]

            if all(palavra in s.lower() for s in sentences):
                examples = [{'sentence': s, 'author': f'- {a}'} for s, a in zip(sentences, authors)]
            else:
                dicioResponse = requests.get(f"https://www.url.com.br/pesquisa.php?q={palavra.lower()}".replace(" ", "-"), headers=headers)
                dicioExamples = BeautifulSoup(dicioResponse.text, features='html.parser')

                if 'Busca' in dicioExamples.text:
                    search_examples = dicioExamples.find("ul", class_='resultados').find('a')
                    url = f"https://www.dicio.com.br{search_examples['href']}"
                    dicioExamples = BeautifulSoup(requests.get(url, headers=headers).text, features='html.parser')

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

                    examples = [{'sentence': s, 'author': a} for s, a in islice(zip(sentences, authors), 5)]
                else:
                    return "Sem exemplos disponíveis"
                    
            '''Retorna um número de 5 exemplos, facilmente customizável
            '''
            return examples[:5]
        except Exception as e:
            return str(e)


