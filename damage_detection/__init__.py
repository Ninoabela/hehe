from flask import Blueprint

damage_bp = Blueprint('damage_bp', __name__,
                      template_folder='templates',
                      static_folder='static')

from . import damage