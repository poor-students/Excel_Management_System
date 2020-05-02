import os

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    UPLOAD_FOLDER = app.instance_path + "\\temp_excels"

    app.config.from_mapping(
        UPLOAD_FOLDER=UPLOAD_FOLDER,
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth
    app.register_blueprint(auth.bp)

    from . import project
    app.register_blueprint(project.bp)

    from . import system
    app.register_blueprint(system.bp)
    app.add_url_rule('/system/', endpoint='import_files')

    return app
