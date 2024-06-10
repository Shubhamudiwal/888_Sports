from flask import Flask
from sportsapp.database import db


def create_app():
    """
        Create and configure the Flask application.

        This function sets up the Flask application with the necessary configurations,
        initializes the database, and registers the main blueprint for the routes.

        Returns:
            Flask: The configured Flask application instance.
    """
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
