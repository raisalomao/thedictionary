from flask import Flask, request, render_template
from flask_caching import Cache
from portuguese.server import BasicInformations


import nltk
import json

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
@cache.cached(timeout=7200)
def palavradodia():
    '''Página principal do site
    '''
    return render_template('home.html')

@app.route('/<palavra>', methods=['GET'])
@cache.cached(timeout=7200)
def principal(palavra):
    '''Executa todo o conjunto de rotas na API
     '''    
    try:
        format_param = request.args.get('format', default='text')
        if format_param.lower() == 'json':
            getResult = json.dumps(BasicInformations.Portuguese(palavra))
            return getResult, 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            getResult = BasicInformations.Portuguese(palavra)
            return str(getResult).encode('utf-8'), 200, {'Content-Type': 'text/plain; charset=utf-8'}
        
    except Exception as e:
            
        return json.dumps(
        {'status' : 404, 'error': f"This word was not found in the Portuguese Dictionary {e}"},
        ensure_ascii=False), {'Content-Type': 'application/json; charset=utf-8'}
    
if __name__ == '__main__':
    nltk.download(['punkt'])
    app.run(debug=True)