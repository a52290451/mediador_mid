import logging
import json
from flask import Response
import yaml

def get_health():
    DicStatus = {
        'Status':'ok',
        'Code':'200'
    }
    return Response(json.dumps(DicStatus),status=200,mimetype='application/json')