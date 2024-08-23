from flask import Blueprint, request, Response
from controllers import healthCheck,intencion
from flask_cors import CORS, cross_origin

def addRouting(app):
    app.register_blueprint(healthCheckController)
    app.register_blueprint(intencionController)


healthCheckController = Blueprint('healthCheckController', __name__, url_prefix='/v1')
CORS(healthCheckController)

@healthCheckController.route('/')
def _():
    return healthCheck.get_health()

# Definición del nuevo controlador
intencionController = Blueprint('intencionController', __name__)
CORS(intencionController)

@intencionController.route('/intencion', methods=['POST'])
@cross_origin()
def _():
    # Obtén los parámetros del cuerpo de la solicitud
    data = request.get_json()
    curso = data.get('curso')
    intencion_d = data.get('intencion')
    pregunta = data.get('pregunta')
    print(data)
    resp = intencion.get_intencion(curso,intencion_d,pregunta)
    # Devolver la respuesta como JSON
    return resp