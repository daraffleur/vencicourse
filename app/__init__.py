import os

from flask import Flask, render_template
from flask_basicauth import BasicAuth
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException

from app.logger import log


# instantiate extensions
login_manager = LoginManager()
db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()
log.set_level(log.DEBUG)
basic_auth = BasicAuth()


def create_app(environment="development"):

    from config import config
    from app.models import (
        Applicant
    )
    from app.views import (
        main_blueprint,
    )

    # Instantiate app.
    app = Flask(__name__, static_folder="assets", static_url_path="/assets")

    # Set app config.
    env = os.environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])
    config[env].configure(app)

    # Set up email.
    mail.init_app(app)

    # Set up extensions.
    db.init_app(app)

    # Set up bootstrap extension
    bootstrap.init_app(app)

    basic_auth.init_app(app)

    # Register blueprints.
    app.register_blueprint(main_blueprint)

    # Set up flask login.
    @login_manager.user_loader
    def get_application(id):
        return Applicant.query.get(int(id))

    login_manager.login_view = "auth.signin"
    login_manager.login_message_category = "info"

    # Error handlers.
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template("error.html", error=exc), exc.code

    return app
