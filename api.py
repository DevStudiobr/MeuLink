from flask import Flask, request, jsonify
import sqlite3
import string
import random

app = Flask(__name__)

# Conectar ao banco de dados
def connect_db():
    conn = sqlite3.connect('urls.db')
    return conn

# Gerar chave curta
def generate_short_key(length=6):
    characters = string.ascii_letters + string.digits
    short_key = ''.join(random.choice(characters) for _ in range(length))
    return short_key

# Rota para encurtar URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('long_url')
    
    if not long_url:
        return jsonify({'error': 'URL longa é necessária'}), 400

    short_key = generate_short_key()
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO urls (long_url, short_key) VALUES (?, ?)', (long_url, short_key))
    conn.commit()
    conn.close()
    
    return jsonify({'short_url': f'http://meulink/{short_key}'})

# Rota para recuperar URL longa
@app.route('/<short_key>', methods=['GET'])
def get_long_url(short_key):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT long_url FROM urls WHERE short_key = ?', (short_key,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({'long_url': result[0]})
    else:
        return jsonify({'error': 'URL não encontrada'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
