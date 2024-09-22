from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Dicionário simples para armazenar URLs
url_storage = {}

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('long_url')

    if not long_url:
        return jsonify({'error': 'URL longa é necessária!'}), 400

    # Criação de um ID simples para a URL encurtada
    short_id = str(len(url_storage) + 1)  # Exemplo simples
    short_url = f"http://meulink/{short_id}"

    # Armazenando a URL
    url_storage[short_id] = long_url

    return jsonify({'short_url': short_url})

@app.route('/<short_id>', methods=['GET'])
def redirect_url(short_id):
    long_url = url_storage.get(short_id)

    if long_url:
        return jsonify({'long_url': long_url})
    else:
        return jsonify({'error': 'URL não encontrada!'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
