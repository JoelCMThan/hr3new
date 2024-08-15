from flask import Blueprint

manager = Blueprint('manager', __name__)

from app.blueprints.manager import routes
