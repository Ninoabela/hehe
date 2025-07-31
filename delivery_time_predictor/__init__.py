from flask import Blueprint

eta_bp = Blueprint('eta_bp', __name__,
                      template_folder='templates',
                      static_folder='static')

from . import eta_module