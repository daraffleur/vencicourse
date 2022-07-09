from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length


class ApplicantForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(1, 100)])
    last_name = StringField("Middle Name", validators=[Length(1, 100)])
    middle_name = StringField("Last Name", validators=[DataRequired(), Length(1, 100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[DataRequired()])
    submit = SubmitField("Send an application")
