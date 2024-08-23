import json
import requests
import pdfkit
import os
import re
import base64
from datetime import datetime  # <-- Agrega esta línea

# Crear la carpeta 'pdfs_agendas' si no existe
output_dir = 'pdfs_agendas'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Cargar el archivo JSON
with open('agenda_data_por_cursos_2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Configuración de wkhtmltopdf
path_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Opciones para configurar wkhtmltopdf
options = {
    'page-size': 'A4',
    'orientation': 'Landscape',
    'encoding': 'UTF-8',
    'no-outline': None
}

# Función para limpiar el nombre del curso
def clean_filename(filename):
    return re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')

# Función para convertir un archivo a base64
def encode_file_to_base64(file_path):
    with open(file_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode('utf-8')

# URL de la API REST donde se almacenarán los PDFs
api_url = 'http://localhost:8082/'

# URLs de la API REST
create_course_url = 'http://localhost:8082/curso'
store_pdf_url = 'http://localhost:8082/recurso'

# Recorrer cada entrada en el JSON y generar un PDF por cada agenda
for entry in data:
    
    course_name = entry['Nombre del curso']
    print(f"Procesando curso: {course_name}")

    # Crear el curso primero
    course_info = {
        "nombre_curso": course_name,
        "periodo_academico": entry.get('Periodo académico', 'N/A'),
        "oferta": entry.get('Oferta', 'N/A'),
        "fecha_creacion": entry.get('Fecha Creación', datetime.utcnow().isoformat() + 'Z'),
        "fecha_modificacion": entry.get('Fecha Modificación', datetime.utcnow().isoformat() + 'Z')
    }

    course_response = requests.post(create_course_url, json=course_info)

    if course_response.status_code == 201:
        # Extraer el ID del curso creado
        course_data = course_response.json().get('Data', {})
        course_id = course_data.get('_id')
        print(course_id)
        if not course_id:
            print(f"No se recibió un ID válido para el curso '{course_name}'.")
            continue

        # Obtener el contenido de la URL para generar el PDF
        url = entry['URL']
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text

            # Crear un archivo temporal HTML para la agenda
            temp_html = f'temp_{clean_filename(course_name)}.html'
            with open(temp_html, 'w', encoding='utf-8') as temp_file:
                temp_file.write('<html><head><style>')
                temp_file.write('body { font-size: 12px; margin: 10px; }')  # Ajustar el tamaño de la fuente y márgenes
                temp_file.write('table, th, td { font-size: 12px; }')  # Ajustar el tamaño de la fuente en tablas
                temp_file.write('</style></head><body>')
                temp_file.write(content)
                temp_file.write('</body></html>')

            # Generar el archivo PDF para la agenda en la carpeta 'pdfs_agendas'
            output_pdf = os.path.join(output_dir, 'agenda.pdf')
            pdfkit.from_file(temp_html, output_pdf, options=options, configuration=config)

            # Limpiar el archivo HTML temporal
            os.remove(temp_html)
            
            print(f"El contenido de la URL se ha guardado en '{output_pdf}'")

            # Convertir el PDF a base64
            encoded_pdf = encode_file_to_base64(output_pdf)

            # Preparar la información del recurso para la API
            resource_info = {
                "curso_id": course_id,
                "nombre": "agenda",
                "descripcion": "Agenda del curso",
                "documento": encoded_pdf,
                "metadatos": {
                    "json" : entry
                },
                "activo": True,
                "fecha_creacion": datetime.utcnow().isoformat() + 'Z',
                "fecha_modificacion": datetime.utcnow().isoformat() + 'Z'
            }

            # Enviar el PDF en formato base64 a través de la API
            pdf_response = requests.post(store_pdf_url, json=resource_info)

            if pdf_response.status_code == 201:
                print(f"El PDF '{output_pdf}' se ha almacenado correctamente a través de la API.")
            else:
                print(f"Error al almacenar el PDF '{output_pdf}' a través de la API. Código de estado: {pdf_response.status_code}")

        else:
            print(f"No se pudo obtener el contenido de la URL: {url}")

    else:
        print(f"Error al crear el curso '{course_name}'. Código de estado: {course_response.status_code}")