from flask import Flask, jsonify
from routers import router
import os

app = Flask(__name__)


router.addRouting(app)

if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 5000))
    app.run(host='0.0.0.0', port=port)