# route_module/__init__.py
from flask import Blueprint

route_bp = Blueprint('route_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/route/static')

from . import views
