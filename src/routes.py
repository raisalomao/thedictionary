from flask import Flask, request, render_template
from flask_caching import Cache
from portuguese.scrapper import BasicInformations
from portuguese.examples import Examples


import nltk
import json

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
@cache.cached(timeout=7200)
def palavradodia():
    return render_template('home.html')

@app.route('/<palavra>')
@cache.cached(timeout=7200)
def principal(palavra):
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
        {'status' : 404, 'error': f"This word was not found {e}"},
        ensure_ascii=False), {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/<palavra>/meanings')
@app.route('/<palavra>/significados')
@cache.cached(timeout=7200)
def significados(palavra):
    try:
        format_param = request.args.get('format', default='text')
        if format_param.lower() == 'json':
            getResult = json.dumps(BasicInformations.orderMeanings(palavra))
            return getResult, 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            getResult = BasicInformations.orderMeanings(palavra)
            return str(getResult).encode('utf-8'), 200, {'Content-Type': 'text/plain; charset=utf-8'}
        
    except Exception as e:
            
        return json.dumps(
        {'status' : 404, 'error': f"This word was not found {e}"},
        ensure_ascii=False), {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/<palavra>/frases')  
@app.route('/<palavra>/examples')
@app.route('/<palavra>/exemplos')
def exemplos(palavra):
    try:
        quant = request.args.get('quant', default = 5, type=int)
        format_param = request.args.get('format', default='text')
        
        if format_param.lower() == 'json':
            getResult = json.dumps(Examples.pensador(palavra.lower(), quant=quant))
            return getResult, 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            getResult = Examples.pensador(palavra.lower(), quant=quant)
            return str(getResult).encode('utf-8'), 200, {'Content-Type': 'text/plain; charset=utf-8'}
        
    except Exception as e:
        return json.dumps(
            {'status' : 404, 'error': f"This word was not found {e}"},
            ensure_ascii=False), {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/<palavra>/synonyms')
@app.route('/<palavra>/sinonimos')
@cache.cached(timeout=7200)
def sinonimos(palavra):
    try:
        format_param = request.args.get('format', default='text')
        
        if format_param.lower() == 'json':
            getResult, i = BasicInformations.wordsRelated(palavra)
            return getResult, 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            getResult, i = BasicInformations.wordsRelated(palavra)
            return str(getResult).encode('utf-8'), 200, {'Content-Type': 'text/plain; charset=utf-8'}
        
    except Exception as e:
        return json.dumps(
            {'status' : 404, 'error': f"This word was not found {e}"},
            ensure_ascii=False), {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/<palavra>/antonyms')
@app.route('/<palavra>/antonimos')
@cache.cached(timeout=7200)
def antonimos(palavra):
    try:
        format_param = request.args.get('format', default='text')
        
        if format_param.lower() == 'json':
            getResult, i = BasicInformations.wordsRelated(palavra)
            return i, 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            getResult, i = BasicInformations.wordsRelated(palavra)
            return str(i).encode('utf-8'), 200, {'Content-Type': 'text/plain; charset=utf-8'}
        
    except Exception as e:
        return json.dumps(
            {'status' : 404, 'error': f"This word was not found {e}"},
            ensure_ascii=False), {'Content-Type': 'application/json; charset=utf-8'}
    

if __name__ == '__main__':
    nltk.download(['punkt'])
    app.run(debug=True)