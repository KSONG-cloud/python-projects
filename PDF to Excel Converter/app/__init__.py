from flask import Flask

# App Factory Pattern
def create_app():
    app = Flask(__name__)

    # App config
    app.config['SECRET_KEY'] = 'your-secret-key'

    # Import routes and register them
    from .routes import main
    app.register_blueprint(main)


    return app


