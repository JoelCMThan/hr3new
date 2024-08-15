from flask import Blueprint

admin = Blueprint('admin', __name__)

from app.blueprints.admin import routes
