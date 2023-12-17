# The Dictionary Project
Coleção de algoritmos de consulta que se conecta a uma ampla variedade de dicionários online distribuídos ao redor do mundo. Fornece uma variedade de recursos, incluindo a obtenção de significados precisos, a separação silábica, a identificação de sinônimos, disponibilização de frases e exemplos contextuais, etimologia e identificação das classes gramaticais.

Destaca-se pela exploração do Processamento de Linguagem Natural. Integrando NLTK (Natural Language Tool Kit), para tarefas de tokenização, classificação e sequenciamento de palavras, para compreender e interpretar o significado e o contexto das palavras pesquisadas.
Desenvolvi uma apresentação visual apartir dos sinônimos obtidos das palavras.

> Representação dos dados em forma hierárquica de árvore, facilitando a navegação, a pesquisa e a manipulação dessas estruturas analíticas. Através do BeautifulSoup e seu parser html.

Descubra a vastidão e complexidade das diferentes línguas através do projeto científico [thedictionary](https://thedictionary.onrender.com/), explorando definições, etimologia e análises linguísticas.

### Simples modo de uso

```py
https://thedictionary.onrender.com/<palavra>?format=json
```

### Endpoints e Responses

*  /palavra/meanings?format=json
*  /palavra/examples?format=json
*  /palavra/synonyms?format=json
*  /palavra/antonyms?format=json

### Exemplos de Resposta Completa

```C
{
    "status": 200,
    "language": "portuguese",
    "results": [
        {
            "word": "dicionário",
            "length": 10,
            "syllables": "di-ci-o-ná-ri-o",
            "gramaticalClass": [
                "substantivo masculino"
            ],
            "meanings": [
                "Compilação que contém as palavras de uma língua, apresentando seu significado, utilização, etimologia, sinônimos, antônimos ou com a tradução para outra língua: dicionário de português; dicionário de português-inglês.",
                "Livro em papel, eletrônico ou em outro formato que possui as informações presentes nessa compilação: O Dicio é um dicionário on-line de língua portuguesa.",
                "Por Extensão. Reunião dos vocábulos ou termos que fazem parte dessa compilação: esta palavra não consta no dicionário.",
                "Por Extensão. Indivíduo que tem um conhecimento excessivo sobre variadas coisas: meu professor é um dicionário que fala."
            ],
            "etymology": "Etimologia (origem da palavra dicionário). A palavra dicionário deriva do latim medieval \"dictionarium\"; pelo francês \"dictionnaire\", que significa repertório de palavras.",
            "sinonimos": [
                "léxico",
                "glossário"
            ],
            "antonyms": [],
            "examples": [
                {
                    "sentence": "Achar que o mundo não tem um criador é o mesmo que afirmar que um dicionário é o resultado de uma explosão numa tipografia.",
                    "author": "- Benjamin Franklin"
                },
                {
                    "sentence": "Também leio livros, muitos livros: mas com eles aprendo menos do que com a vida. Apenas um livro me ensinou muito: o dicionário. Oh, o dicionário, adoro-o. Mas também adoro a estrada, um dicionário muito mais maravilhoso.",
                    "author": "- Ettore Petrolini"
                }
            ]
        }
    ]
}
```

O formato padrão de resposta é texto, utilize o parâmetro JSON para retornar um formato de dados mais leve e utilizável para outras aplicações.
