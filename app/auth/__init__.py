"""
Authentication Blueprint
"""
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from . import views