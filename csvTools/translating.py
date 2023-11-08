 
import requests
import json

# Función para traducir una línea
def traducir_linea(linea, lang="en"):
    linea = linea.strip() 
     
    url = "http://localhost:5000/translate"

    # Datos para enviar en la solicitud POST
    data = {
        "q": linea,
        "source": "auto",
        "target": lang,
        "format": "text",
        "api_key": ""
    }

    # Encabezados de la solicitud
    headers = {
        "Content-Type": "application/json"
    } 
    response = requests.post(url, data=json.dumps(data), headers=headers)
 
    if response.status_code == 200: 
        response_data = response.json() 
        return(response_data['translatedText'])
    else:
        print(f"Error: Código de respuesta {response.status_code}")
 
