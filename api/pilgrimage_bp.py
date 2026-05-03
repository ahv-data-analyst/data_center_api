from flask import Blueprint, g, jsonify

pilgrimage_bp = Blueprint("pilgrimage", __name__)

@pilgrimage_bp.route('/')
def get_all():
    pass