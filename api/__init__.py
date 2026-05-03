from flask import Flask, g
from database.database_manager import DatabaseManager
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow all origins, or:
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    @app.before_request
    def open_db():
        g.db_manager = DatabaseManager("data/ahv_data.db")
        g.db = g.db_manager.__enter__()  # Open connection

    @app.teardown_appcontext
    def close_db(exception=None):
        if hasattr(g, 'db_manager'):
            g.db_manager.__exit__(None, None, None)  # Close safely
            
    from api.app import main_bp
    from api.assessment_bp import assessment_bp
    from api.members_bp import members_bp
    from api.pilgrimage_bp import pilgrimage_bp
    
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(assessment_bp, url_prefix='/assessments')
    app.register_blueprint(members_bp, url_prefix='/members')
    app.register_blueprint(pilgrimage_bp, url_prefix='/pilgrimage')
    return app