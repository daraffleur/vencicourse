import os
import requests

from flask import render_template, request, Blueprint, flash, redirect

from app.forms import ApplicantForm
from app.models import Applicant
from app.logger import log


main_blueprint = Blueprint("main", __name__)
EMAIL_ENDPOINT = os.environ.get("EMAIL_ENDPOINT")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_applicant_to_telegram_chat(text):
    method = "sendMessage"
    token = TELEGRAM_TOKEN
    chat_id = TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

@main_blueprint.route("/", methods=["GET", "POST"])
def index():
    form = ApplicantForm(request.form)
    if form.validate_on_submit():
        applicant = Applicant(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
        )
        applicant.save()
        applicant = f"NEW APPLICATION \n\nFirst Name: {form.first_name.data}\nLast Name: {form.last_name.data}\n \nEmail: {form.email.data}\nPhone Number: {form.phone.data}"
        send_applicant_to_telegram_chat(applicant)
        flash(
            "Your application has been sent successfully! We will call you soon!",
            "success",
        )
        log(
            log.DEBUG,
            "Your application has been sent successfully! We will call you soon!",
        )
        return redirect("http://www.coursebyvencistankov.info/#registration")
    elif form.is_submitted():
        for error in form.errors:
            for msg in form.errors[error]:
                log(log.ERROR, "Save application(): %s", msg)
                flash(
                    "Something went wrong... Please reload the page and try submitting an application again. ",
                    "danger",
                )
                return redirect("http://www.coursebyvencistankov.info/#registration")
    return render_template("index.html", form=form)
