import sqlite3
from bottle import request, response, run, post

@post('/to-file')
def to_file():
    data = request.forms.get('data')

    if not data:
        response.status = 400
        return {"error": "No data"}

    with open('task6.txt', "a") as f:
        f.write(data + "\n")
    return {"message": "Data added to file"}

@post('/to-db')
def to_db():
    data = request.forms.get('data')

    if not data:
        response.status = 400
        return {"error": "No data"}

    connection = sqlite3.connect('task6.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL
    )''')
    cursor.execute('INSERT INTO Records (data) VALUES (?)', (data,))
    connection.commit()
    connection.close()
    return {"message": "Data added to database"}

if __name__ == "__main__":
    run(host='localhost', port=8000)
