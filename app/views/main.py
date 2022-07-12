import os

from flask import render_template, request, Blueprint, flash, redirect

from app.forms import ApplicantForm
from app.models import Applicant
from app.logger import log


main_blueprint = Blueprint("main", __name__)
EMAIL_ENDPOINT = os.environ.get("EMAIL_ENDPOINT")


# def send_applicant_to_telegram_chat(text):
#     method = "sendMessage"
#     token = "2049371679:AAGLoC9AaUdNAaxrsgCYOEF15kiXZmRVTq8"
#     chat_id = "-1001398146536"
#     url = f"https://api.telegram.org/bot{token}/{method}"
#     data = {"chat_id": chat_id, "text": text}
#     requests.post(url, data=data)


@main_blueprint.route("/", methods=["GET", "POST"])
def index():
    form = ApplicantForm(request.form)
    if form.validate_on_submit():
        # applicant = f"НОВА ЗАЯВКА НА КУРС\n\nПрізвище: {form.first_name.data}\nІм'я: {form.last_name.data}\n \nЕмейл: {form.email.data}\nНомер телефону: {form.phone.data}"
        # send_applicant_to_telegram_chat(applicant)
        applicant = Applicant(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
        )
        applicant.save()
        flash(
            "Your application has been sent successfully! We will call you soon!",
            "success",
        )
        log(
            log.DEBUG,
            "Your application has been sent successfully! We will call you soon!",
        )
        # return redirect("https://tokarstudy.com.ua/#registration")
        return redirect("http://localhost:5000/#registration")
    elif form.is_submitted():
        for error in form.errors:
            for msg in form.errors[error]:
                log(log.ERROR, "Save application(): %s", msg)
                flash(
                    "Something went wrong... Please reload the page and try submitting an application again. ",
                    "danger",
                )
                # return redirect("https://tokarstudy.com.ua/#registration")
                return redirect("http://localhost:5000/#registration")
    return render_template("index.html", form=form)
