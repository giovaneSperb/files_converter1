import os

from flask import Flask

from config import Config


def create_app():

    app = Flask(
        __name__
    )

    app.config.from_object(
        Config
    )

    os.makedirs(
        app.config[
            "UPLOAD_FOLDER"
        ],
        exist_ok=True
    )

    os.makedirs(
        app.config[
            "OUTPUT_FOLDER"
        ],
        exist_ok=True
    )

    from app.routes.pagamentos_routes import (
        pagamentos_bp
    )

    app.register_blueprint(
        pagamentos_bp,
        url_prefix="/api/pagamentos"
    )

    return app