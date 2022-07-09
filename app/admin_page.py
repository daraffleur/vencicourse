from app.models.applicant import Applicant
from flask import (
    Response,
    redirect,
)
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin.base import expose, AdminIndexView

# from flask_security import current_user
from werkzeug.exceptions import HTTPException


from app import basic_auth
from app.models import Applicant
from app.logger import log


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(
            message,
            Response(
                "You could not be authenticated. Please refresh the page.",
                401,
                {"WWW-Authenticate": 'Basic realm="Login Required"'},
            ),
        )


class MyView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render("admin_page/index.html")


class ApplicationModelView(sqla.ModelView):
    # column_filters = [
    #     "title",
    #     "url",
    #     "available_to_unregistered_user",
    #     "available_to_registered_user",
    #     "role",
    # ]

    # def is_accessible(self):
    #     return current_user.role != "admin"

    def is_accessible(self):
        if not basic_auth.authenticate():
            log(log.WARNING, "Not authenticated.")
            raise AuthException("Not authenticated.")
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


def init_admin(app, db):
    admin = Admin(
        app,
        template_mode="bootstrap3",
    )
    admin.add_views(ApplicationModelView(Applicant, db.session))
    return admin
