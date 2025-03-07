from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

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

@app.route('/buscar', methods=['GET'])
def buscar():
    item = request.args.get('item', '')
    categoria = request.args.get('categoria', '')
    
    # Mapeo de categorías a endpoints
    endpoints = {
        'productos': f"{BASE_URL}/productos_code.json?combine_prod={item}&page=0",
        'segmentos': f"{BASE_URL}/segmentos_code.json?combine_segmento={item}&page=0",
        'familias': f"{BASE_URL}/familias_code.json?combine_familia={item}&page=0",
        'clases': f"{BASE_URL}/clases_code.json?combine_clase={item}&page=0"
    }
    
    try:
        url = endpoints.get(categoria, '')
        if not url:
            return jsonify({'error': 'Categoría no válida'}), 400
            
        print(f"Realizando petición a: {url}")  # Para debug
        response = requests.get(
            url,
            headers=headers,
            cookies=cookies,
            verify=True  # Asegura verificación SSL
        )
        
        # Imprimir información de debug
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        response.raise_for_status()
        return jsonify(response.json())
        
    except requests.RequestException as e:
        print(f"Error en la petición: {str(e)}")  # Para debug
        return jsonify({'error': str(e)}), 500

@app.route('/buscar_todo', methods=['GET'])
def buscar_todo():
    item = request.args.get('item', '')
    
    # Endpoints para todas las categorías
    endpoints = {
        'productos': f"{BASE_URL}/productos_code.json?combine_prod={item}&page=0",
        'segmentos': f"{BASE_URL}/segmentos_code.json?combine_segmento={item}&page=0",
        'familias': f"{BASE_URL}/familias_code.json?combine_familia={item}&page=0",
        'clases': f"{BASE_URL}/clases_code.json?combine_clase={item}&page=0"
    }
    
    resultados = {}
    
    try:
        for categoria, url in endpoints.items():
            print(f"Consultando {categoria} en: {url}")  # Debug
            response = requests.get(
                url,
                headers=headers,
                cookies=cookies,
                verify=True
            )
            response.raise_for_status()
            datos = response.json()
            # Asegurarse de que los datos son una lista
            resultados[categoria] = datos if isinstance(datos, list) else []
            print(f"Respuesta para {categoria}: {response.status_code}")  # Debug
            
        return jsonify(resultados)
        
    except requests.RequestException as e:
        print(f"Error en la petición: {str(e)}")  # Debug
        return jsonify({'error': str(e)}), 500

@app.route('/obtener_segmentos', methods=['GET'])
def obtener_segmentos():
    try:
        # URL correcta para obtener segmentos
        url = "https://www.colombiacompra.gov.co/clasificador/segmentos.json"
        response = requests.get(
            url,
            headers=headers,  # Ahora usa las variables globales
            cookies=cookies,
            verify=True
        )
        response.raise_for_status()
        datos = response.json()
        
        # Transformar los datos al formato esperado
        segmentos_formateados = [
            {
                "cod_segmento": str(segmento.get("id", "")),
                "nom_segmento": segmento.get("description", "")
            }
            for segmento in datos
        ]
        
        # Agregar opción "Todos los segmentos" al inicio
        return jsonify([{"cod_segmento": "0", "nom_segmento": "Todos los segmentos"}] + segmentos_formateados)
    except requests.RequestException as e:
        print(f"Error obteniendo segmentos: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/buscar_por_segmento', methods=['GET'])
def buscar_por_segmento():
    item = request.args.get('item', '')
    segmento = request.args.get('segmento', '')
    
    try:
        if (segmento == "0"):  # Todos los segmentos
            url = f"https://www.colombiacompra.gov.co/clasificador/productos.json?producto={item}"
        else:
            url = f"https://www.colombiacompra.gov.co/clasificador/productos.json?producto={item}&segmento={segmento}"
            
        response = requests.get(
            url,
            headers=headers,
            cookies=cookies,
            verify=True
        )
        response.raise_for_status()
        return jsonify(response.json())
        
    except requests.RequestException as e:
        print(f"Error en la búsqueda: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
