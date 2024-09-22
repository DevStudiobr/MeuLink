import sqlite3
import string
import random

# Função para conectar ao banco de dados
def connect_db():
    conn = sqlite3.connect('urls.db')
    return conn

# Função para criar a tabela URLs, caso não exista
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            short_key TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para gerar uma chave curta (ex: abc123)
def generate_short_key(length=6):
    characters = string.ascii_letters + string.digits
    short_key = ''.join(random.choice(characters) for _ in range(length))
    return short_key

# Função para encurtar a URL
def shorten_url(long_url):
    conn = connect_db()
    cursor = conn.cursor()

    # Gerar a chave curta
    short_key = generate_short_key()

    # Verificar se a chave já existe
    cursor.execute('SELECT * FROM urls WHERE short_key = ?', (short_key,))
    while cursor.fetchone() is not None:
        short_key = generate_short_key()

    # Inserir a URL no banco de dados
    cursor.execute('INSERT INTO urls (long_url, short_key) VALUES (?, ?)', (long_url, short_key))
    conn.commit()
    conn.close()

    return f"http://meulink/{short_key}"

# Função para recuperar a URL longa
def get_long_url(short_key):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT long_url FROM urls WHERE short_key = ?', (short_key,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return None

# Menu interativo
def main():
    create_table()
    print("Bem-vindo ao Encurtador de URL")

    while True:
        print("\nOpções:")
        print("1. Encurtar uma URL")
        print("2. Recuperar uma URL longa")
        print("3. Sair")
        
        choice = input("Escolha uma opção: ")

        if choice == '1':
            long_url = input("Digite a URL longa (com http:// ou https://): ")
            short_url = shorten_url(long_url)
            print(f"URL encurtada: {short_url}")

        elif choice == '2':
            short_key = input("Digite a chave curta da URL: ")
            long_url = get_long_url(short_key)
            if long_url:
                print(f"URL longa: {long_url}")
            else:
                print("URL não encontrada.")
        
        elif choice == '3':
            print("Saindo...")
            break
        
        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == '__main__':
    main()
