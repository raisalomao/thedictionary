# The Dictionary Project
Coleção de algoritmos de consulta que se conecta a uma ampla variedade de dicionários online distribuídos ao redor do mundo. Fornece uma variedade de recursos, incluindo a obtenção de significados precisos, a separação silábica, a identificação de sinônimos, disponibilização de frases e exemplos contextuais, etimologia e identificação das classes gramaticais.

Destaca-se pela exploração do Processamento de Linguagem Natural. Integrando NLTK (Natural Language Tool Kit), para tarefas de tokenização, classificação e sequenciamento de palavras, para compreender e interpretar o significado e o contexto das palavras pesquisadas.
Desenvolvi uma apresentação visual apartir dos sinônimos obtidos das palavras.

> Representação dos dados em forma hierárquica de árvore, facilitando a navegação, a pesquisa e a manipulação dessas estruturas analíticas. Através do BeautifulSoup e seu parser html.

Descubra a vastidão e complexidade das diferentes línguas através do projeto científico [thedictionary](https://thedictionary.onrender.com/), explorando definições, etimologia e análises linguísticas.

###Simples modo de uso

```py
https://thedictionary.onrender.com/<palavra>?format=json
```

###Endpoints e Responses

>  /meanings?format=json
>  /examples?format=json
>  /synonyms?format=json
>  /antonyms?format=json

O formato padrão de resposta é texto, utilize o parâmetro JSON para retornar um formato de dados mais leve e utilizável para outras aplicações.
