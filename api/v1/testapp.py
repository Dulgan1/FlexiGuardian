#!/usr/bin/python3
""" Creates api test app """
from api.v1.views import api_views
from flask import Flask
from flask_cors import CORS
from os import getenv
from models import storage

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('FG_SECRET_KEY')
app.register_blueprint(api_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_storage(error):
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

if __name__ == '__main__':
    app.run(host='localhost', port='5000')
