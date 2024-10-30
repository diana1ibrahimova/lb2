from bottle import request, response, route, run

@route('/currency')
def text_format():
    content_type = request.get_header('Content-Type')

    if content_type == 'application/json':
        response.content_type = 'application/json'
        return {"message": "JSON response"}
    elif content_type == 'application/xml':
        response.content_type = 'application/xml'
        return "<response><message> XML response</message></response>"
    else:
        return "plaintext response"

if __name__ == "__main__":
    run(host='localhost', port=8000)
