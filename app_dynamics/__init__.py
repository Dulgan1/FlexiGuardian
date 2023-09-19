""" App view 
    Blueprint """
from flask import Blueprint

app_views = Blueprint('app_views', __name__)

from app_dynamics.login import *
from app_dynamics.register import *
from app_dynamics.contract import *
from app_dynamics.auth import *
