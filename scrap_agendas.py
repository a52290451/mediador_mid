import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import docx

# Cargar el archivo Excel
excel_file = 'carga_masiva_prueba_1.xlsx'  # Cambiar por la ruta de tu archivo Excel
df = pd.read_excel(excel_file, sheet_name='Hoja1')

# URL base común para todas las agendas
base_url = 'https://datateca.unad.edu.co/contenidos/agendas/2024-1701/'

# Lista para almacenar todos los datos de los cursos
all_courses_data = []

# Definir encabezados
headers = [
    "Momento de la e-evaluación", "Nombre de la unidad", "Nombre de la actividad", 
    "Descripción de la actividad", "Tipo de actividad", "Peso evaluativo (en puntajes)", 
    "Actividad inicia en:", "Actividad finaliza en:", "Alerta de cierre en:", 
    "Fecha de entrega realimentación"
]

# Recorrer cada código de curso en la columna "curso"
for curso in df['Curso']:
    # Construir la URL específica para este curso
    url = base_url + str(curso) + '.htm'


    # Realiza una solicitud GET a la página web
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:

        # Analiza el contenido HTML de la página web
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encuentra el <h1> que contiene "Agenda del curso"
        h1_tag = soup.find('h1', text='Agenda del curso')
        h2_tag = soup.find('h2', text='período académico:')

        # Si se encuentra el <h1> correcto, busca el <p> inmediatamente siguiente
        if h1_tag:
            # Encuentra el siguiente <p> después del <h1>
            course_name_tag = h1_tag.find_next('p')
            course_name = course_name_tag.text.strip() if course_name_tag else 'No disponible'
        else:
            course_name = 'No disponible'

        if h2_tag:
            # Encuentra el siguiente <p> después del <h1>
            academic_period_tag = h2_tag.find_next('p')
            academic_period = academic_period_tag.text.strip() if academic_period_tag else 'No disponible'
        else:
            academic_period = 'No disponible'

        title = soup.find('title')
        titulo = title.text.strip() if title else 'No disponible'

        # Encuentra todas las filas de la tabla
        table_rows = soup.select('table tr')

        # Lista para almacenar todos los momentos
        momentos = {}

        # Variables para almacenar el valor actual de "Momento de la e-evaluación" y "Nombre de la unidad"
        current_momento = None
        current_unidad = None

        # Recorre las filas omitiendo la primera que es el header de la tabla
        for row in table_rows[2:]:
            columns = row.find_all('td')

            # Verifica la cantidad de TDs en la fila
            num_columns = len(columns)

            # Si no tiene TDs o menos de 8, omitir la fila
            if num_columns == 0 or num_columns < 8:
                continue
            
            # Si tiene 10 o 9 TDs, actualiza la última unidad válida
            if num_columns == 10:
                current_momento = columns[0].text.strip()
                current_unidad = columns[1].text.strip()
                index = 2

            if num_columns == 9:
                current_unidad = columns[0].text.strip()
                index = 1
            
            if num_columns == 8:
                index = 0
            
            # Crear diccionario de la actividad con los valores actuales
            activity = {
                headers[2]: columns[index ].text.strip(),
                headers[3]: columns[index + 1 ].text.strip(),
                headers[4]: columns[index + 2 ].text.strip(),
                headers[5]: columns[index + 3 ].text.strip(),
                headers[6]: columns[index + 4 ].text.strip(),
                headers[7]: columns[index + 5 ].text.strip(),
                headers[8]: columns[index + 6 ].text.strip(),
                headers[9]: columns[index + 7 ].text.strip()
            }

            # Si el momento no existe, inicializa su lista
            if current_momento not in momentos:
                momentos[current_momento] = {}
            
            # Si la unidad no existe, inicializa su lista
            if current_unidad not in momentos[current_momento]:
                momentos[current_momento][current_unidad] = []
            
            # Añadir la actividad a la unidad del momento
            momentos[current_momento][current_unidad].append(activity)

        # Estructura final en JSON
        agenda_data = {
            'URL': url,
            'Nombre del curso': course_name,
            'Periodo académico': academic_period,
            'titulo': titulo,
            'Momentos': momentos
        }

        # Agregar los datos del curso actual a la lista de todos los cursos
        all_courses_data.append(agenda_data)
    else:
        print(f"No se pudo acceder a la URL: {url}")


# Almacenar todos los datos en un archivo JSON
with open('agenda_data_por_cursos_2.json', 'w', encoding='utf-8') as f:
    json.dump(all_courses_data, f, ensure_ascii=False, indent=4)

print('Datos almacenados en agenda_data.json')