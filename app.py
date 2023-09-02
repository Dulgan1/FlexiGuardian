#!usr/bin/python3
"""  FlexiGuardian Main App"""
from flask import Flask, render_template
from flask_cors import CORS
from api.v1.views import api_views
from app_dynamics import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.register_blueprint(api_views)
app.config['SECRET_KEY'] = getenv('FG_SECRET_KEY')
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.teardown_appcontext
def close_storage(error):
    storage.close()

@app.errorhandler(404)
def error404():
    return render_template('app_dynamics/templates/404.html')

if __name__ == '__main__':
    app.run(host='localhost', port='5000')
