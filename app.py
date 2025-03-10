import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Configuración para Railway/Vercel
port = int(os.getenv('PORT', 8080))  # Cambiado de 5000 a 8080
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

@app.route('/api/buscar/productos', methods=['GET'])
def buscar_productos():
    try:
        query = request.args.get('combine_prod', '')
        page = request.args.get('page', '0')
        
        url = f"{BASE_URL}/productos_code.json"
        params = {
            'combine_prod': query,
            'page': page
        }
        
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        response.raise_for_status()  # Lanzará una excepción si hay error HTTP
        
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/buscar/clases', methods=['GET'])
def buscar_clases():
    try:
        query = request.args.get('combine_clase', '')
        page = request.args.get('page', '0')
        
        url = f"{BASE_URL}/clases_code.json"
        params = {
            'combine_clase': query,
            'page': page
        }
        
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        response.raise_for_status()
        
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/buscar/familias', methods=['GET'])
def buscar_familias():
    try:
        query = request.args.get('combine_familia', '')
        page = request.args.get('page', '0')
        
        url = f"{BASE_URL}/familias_code.json"
        params = {
            'combine_familia': query,
            'page': page
        }
        
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        response.raise_for_status()
        
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/buscar/segmentos', methods=['GET'])
def buscar_segmentos():
    try:
        query = request.args.get('combine_segmento', '')
        page = request.args.get('page', '0')
        
        url = f"{BASE_URL}/segmentos_code.json"
        params = {
            'combine_segmento': query,
            'page': page
        }
        
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        response.raise_for_status()
        
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/buscar', methods=['GET'])
def buscar():
    try:
        item = request.args.get('item', '')
        categoria = request.args.get('categoria', 'productos')
        
        # Mapeo de categorías a endpoints
        endpoints = {
            'productos': 'productos_code.json',
            'clases': 'clases_code.json',
            'familias': 'familias_code.json',
            'segmentos': 'segmentos_code.json'
        }
        
        # Mapeo de parámetros de búsqueda
        param_names = {
            'productos': 'combine_prod',
            'clases': 'combine_clase',
            'familias': 'combine_familia',
            'segmentos': 'combine_segmento'
        }
        
        if categoria not in endpoints:
            return jsonify({'error': 'Categoría no válida'}), 400
            
        url = f"{BASE_URL}/{endpoints[categoria]}"
        params = {
            param_names[categoria]: item,
            'page': '0'
        }
        
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Asegurarse de que la respuesta sea una lista
        if isinstance(data, dict) and 'items' in data:
            return jsonify(data['items'])
        return jsonify(data)
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error de conexión: {str(e)}'}), 500
    except ValueError as e:
        return jsonify({'error': f'Error al procesar JSON: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@app.route('/buscar_todo', methods=['GET'])
def buscar_todo():
    try:
        item = request.args.get('item', '')
        resultados = {}
        
        categorias = {
            'productos': 'combine_prod',
            'clases': 'combine_clase',
            'familias': 'combine_familia',
            'segmentos': 'combine_segmento'
        }
        
        for categoria, param_name in categorias.items():
            url = f"{BASE_URL}/{categoria}_code.json"
            params = {param_name: item, 'page': '0'}
            
            try:
                response = requests.get(url, headers=headers, cookies=cookies, params=params)
                response.raise_for_status()
                resultados[categoria] = response.json()
            except:
                resultados[categoria] = []
                
        return jsonify(resultados)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Asegurarse de que el puerto sea un entero
    port = int(os.getenv('PORT', 8080))  # Cambiado de 5000 a 8080
    # Configuración para producción
    app.run(host='0.0.0.0', port=port)
