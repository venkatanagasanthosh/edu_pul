from flask import Flask
from flask_migrate import Migrate
from config import Config
from db import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprints
    from routes import routes_bp, admin_bp
    app.register_blueprint(routes_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
