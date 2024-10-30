from bottle import route, run, request

@route ('/currency')
def get_currency():
    if 'today' in request.query:
        return "Today exchange rate is 41.5"
    if 'yesterday' in request.query :
         return "Yesterday exchange rate is 41.7"

    return 'Unknown query. Supported queries is are /currency?today or /currency?yesterday'

if __name__ == '__main__':
    run(host='localhost', port=8000)
