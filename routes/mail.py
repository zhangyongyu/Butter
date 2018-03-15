from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *
from models.mail import Mail

main = Blueprint('mail', __name__)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    Mail.new(form, sender_id=u.id)
    return redirect(url_for(".index"))


@main.route("/", methods=["GET"])
def index():
    u = current_user()
    send_mail = Mail.all(sender_id=u.id)
    received_mail = Mail.all(receiver_id=u.id)
    t = render_template(
        "mail/index.html",
        sends=send_mail,
        receives=received_mail
    )
    return t


@main.route("/view/<string:id>")
def view(id):
    mail = Mail.one(id)
    if current_user().id in [mail.receiver_id, mail.sender_id]:
    # if current_user().id == mail.receiver_id and current_user().id == mail.sender_id:
        return render_template("mail/detail.html", mail=mail)
    else:
        return redirect(url_for(".index"))
