from flask import Flask
from sportsapp.database import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from sportsapp.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


app = create_app()
