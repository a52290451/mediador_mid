# mediador_mid

API MID para la gestión de interacciones con intención especializadas para cursos ChatBot.

## Especificaciones Técnicas

### Tecnologías Implementadas y Versiones
* [Flask (Python)](https://flask.palletsprojects.com/en/1.1.x/)
* [Gemini API](https://ai.google.dev/)

### Variables de Entorno
```shell
# parametros de api
API_PORT=[Puerto de exposición del API]
```

**NOTA:** Las variables se pueden ver en el fichero api.py ...

### Ejecución del Proyecto
```shell
#1. Obtener el repositorio con git
git clone https://github.com/a52290451/mediador_mid.git

#2. Moverse a la carpeta del repositorio
cd mediador_mid

# 3. Moverse a la rama **develop**
git pull origin develop && git checkout develop

# 4. alimentar todas las variables de entorno que utiliza el proyecto.
export API_PORT=8080

# 5. instalar dependencias de python
pip3 install -r requirements.txt

# 6. Ejecutar el api
python3 api.py
```

### Documentacion

- 
