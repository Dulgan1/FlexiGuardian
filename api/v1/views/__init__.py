#!/usr/bin/python3
from flask import Blueprint
from models import storage

api_views = Blueprint('api_views', __name__, url_prefix='/api/v1')

from api.v1.views.user import *
from api.v1.views.contract import * #TODO: Complete the code
from api.v1.views.token import *

def calc_tot_rate(user_id):
    user = storage.get(User, user_id)
    _session = storage.session()
    reviews = _session.query(Review).filter(Review.for_user_id==user_id)
    total = 0
    count = 0
    for review in reviews:
        total += review.rating
        count += 1
    rate_tot = total / count                                                            
    user.rating = rate_tot
    storage.save
