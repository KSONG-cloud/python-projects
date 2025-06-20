import os

from flask import Flask

def create_app(test_config=None):
    # Create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)


    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # A simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    


    # Database Creation
    from . import db
    db.init_app(app)


    # Importing and registering authentication blueprint
    from . import auth
    app.register_blueprint(auth.bp)


    # Importing and registering blog blueprint
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

