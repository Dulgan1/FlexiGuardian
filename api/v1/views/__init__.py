#!/usr/bin/python3
from flask import Blueprint
from models import storage

api_views = Blueprint('api_views', __name__, url_prefix='/api/v1')

from api.v1.views.user import *
from api.v1.views.contract import * #TODO: Complete the code
from api.v1.views.token import *
