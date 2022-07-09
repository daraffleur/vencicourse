from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError,
    SelectField,
)

app = Flask(__name__, static_folder="assets", static_url_path="/assets")


@app.route('/')
def hello():
    return render_template("index.html")


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
