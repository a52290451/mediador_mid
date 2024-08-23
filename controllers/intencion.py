import logging
import requests
import json
from flask import Response
import google.generativeai as genai
import os

# Configuración de logging
logging.basicConfig(level=logging.INFO)

# URL de la API externa
API_URL = 'http://localhost:8082/'

# Configuración de la clave de API de Google Generative AI
GENAI_API_KEY = os.getenv("GENAI_API_KEY", "AIzaSyDDJ4BTk9jWbpKfUQOSAZY0dcQOK7Ynb3g")  # Asegúrate de tener la clave en las variables de entorno

def fetch_data_from_api(endpoint, query):
    """Realiza una solicitud GET a la API externa y devuelve la respuesta en formato JSON."""
    url = f"{API_URL}{endpoint}?{query}"
    logging.info(f"Requesting URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise

def get_intencion(curso, intencion, pregunta):
    """Obtiene los metadatos de un curso y responde a una pregunta utilizando Google Generative AI."""
    try:
        # Obtener el ID del curso
        curso_data = fetch_data_from_api("curso", f"query=nombre_curso:{curso}")
        if curso_data.get("Success") and curso_data.get("Data"):
            id_curso = curso_data["Data"][0].get("_id")
        else:
            return Response(json.dumps({"error": "ID de curso no encontrado en la respuesta"}), status=404, mimetype='application/json')

        # Obtener los metadatos del recurso
        recurso_data = fetch_data_from_api("recurso", f"query=curso_id:{id_curso}&nombre:{intencion}")
        if recurso_data.get("Success") and recurso_data.get("Data"):
            metadatos = recurso_data["Data"][0].get("metadatos", "sin metadatos")
        else:
            return Response(json.dumps({"error": "Metadatos no encontrados en la respuesta"}), status=404, mimetype='application/json')

        # Configurar Google Generative AI
        genai.configure(api_key=GENAI_API_KEY)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        # Generar contenido
        response = model.generate_content(
            f"Tengo la siguiente información: {metadatos}. Con base en la información anterior, "
            f"teniendo en cuenta que es para un estudiante, responde la siguiente pregunta: {pregunta}"
        )
        logging.info(f"Generative AI response: {response.text}")

        return Response(json.dumps({"metadatos": metadatos}), status=200, mimetype='application/json')

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        error_message = {"error": str(e)}
        return Response(json.dumps(error_message), status=500, mimetype='application/json')