import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv


load_dotenv()


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'




def create_app(config_object=None):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///portfy.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)


    # Blueprints
    from .views.auth import auth_bp
    from .views.dashboard import dash_bp
    from .views.public import public_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)
    app.register_blueprint(public_bp)


    # Create DB tables if not exist
    with app.app_context():
        db.create_all()


        return app