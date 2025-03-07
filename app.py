import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Configuración para Railway
port = os.getenv('PORT', 5000)
BASE_URL = "https://www.colombiacompra.gov.co/clasificador"

# Headers globales
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'www.colombiacompra.gov.co',
    'Referer': 'https://www.colombiacompra.gov.co/clasificador-de-bienes-y-servicios',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0'
}

# Cookies globales
cookies = {
    'has_js': '1',
    '_ga': 'GA1.3.1334865225.1741357431',
    '_gid': 'GA1.3.713288181.1741357431',
    '_ga_9ELSKQF488': 'GS1.3.1741365345.3.0.1741365345.60.0.0',
    '_ga_6B7EM2S9HE': 'GS1.3.1741365345.3.0.1741365345.0.0.0',
    '_fbp': 'fb.2.1741357432475.874066690923338085'
}

@app.route('/')
def home():
    return render_template('index.html')

# ...existing endpoints code...

if __name__ == '__main__':
    # Asegurarse de que el puerto sea un entero
    port = int(os.getenv('PORT', 5000))
    # Configuración para producción
    app.run(host='0.0.0.0', port=port)
