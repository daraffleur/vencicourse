import os
import requests
from flask import render_template, request, Blueprint, flash, redirect
from app.forms import ApplicantForm
from app.models import Applicant
from app.logger import log


main_blueprint = Blueprint("main", __name__)
EMAIL_ENDPOINT = os.environ.get("EMAIL_ENDPOINT")


def send_applicant_to_telegram_chat(text):
    method = "sendMessage"
    token = "2049371679:AAGLoC9AaUdNAaxrsgCYOEF15kiXZmRVTq8"
    chat_id = "-1001398146536"
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


@main_blueprint.route("/", methods=["GET", "POST"])
def index():
    form = ApplicantForm(request.form)
    if form.validate_on_submit():
        applicant = f"НОВА ЗАЯВКА НА КУРС\n\nПрізвище: {form.first_name.data}\nІм'я: {form.last_name.data}\nПо батькові: {form.middle_name.data}\nЕмейл: {form.email.data}\nНомер телефону: {form.phone.data}"
        send_applicant_to_telegram_chat(applicant)
        applicant = Applicant(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            middle_name=form.middle_name.data,
            email=form.email.data,
            phone=form.phone.data,
        )
        applicant.save()
        flash("Ваша заявка відправлена успішно! Ми вам зателефонуємо!", "success")
        log(log.DEBUG, "Ваша заявка відправлена успішно! Ми вам зателефонуємо!")
        return redirect("https://tokarstudy.com.ua/#registration")
    elif form.is_submitted():
        for error in form.errors:
            for msg in form.errors[error]:
                log(log.ERROR, "Save application(): %s", msg)
                flash(
                    "Щось пішло не так... Будь ласка, перезавантажте сторінку і спробуйте відправити заявку на курс ще раз. ",
                    "danger",
                )
                return redirect("https://tokarstudy.com.ua/#registration")
    return render_template("index.html", form=form)
