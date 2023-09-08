#!usr/bin/python3
"""  FlexiGuardian Main App"""
from flask import Flask, render_template
#from flask_cors import CORS
from models import storage
from api.v1.views import api_views
from app_dynamics import app_views
from os import getenv

app = Flask(__name__, template_folder='app_dynamics/templates')
app.register_blueprint(app_views)
app.register_blueprint(api_views)
app.config['SECRET_KEY'] = getenv('FG_SECRET_KEY')
#cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.teardown_appcontext
def close_storage(error):
    storage.close()

@app.errorhandler(404)
def error404(error):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
