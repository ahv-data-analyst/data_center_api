from flask import Blueprint, jsonify

main_bp = Blueprint("app", __name__)

@main_bp.route("/")
def health_check():
    return jsonify({
        "Service": "AHV DATA CENTER",
        "Health": "Healthy"
    }), 200