from flask import Blueprint

employee = Blueprint('employee', __name__)

from app.blueprints.employee import routes
