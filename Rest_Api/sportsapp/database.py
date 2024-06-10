from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """
    Initialize the database with the given Flask application.

    This function sets up the SQLAlchemy extension to work with the Flask app,
    and creates all the necessary database tables.

    Args:
        app (Flask): The Flask application instance to initialize the database with.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
