from flask import (
    Flask,
    render_template,
    request,
)

from scripts import DBSession
from models import Database, PEP, Status, User
import os

app = Flask(__name__)
db = Database() if os.path.abspath(os.getcwd()).endswith("app") else Database("app")


@app.errorhandler(404)
def handle_404(err):
    return render_template("404_error.html", url=request.path), 404


@app.errorhandler(500)
def handle_500(err):
    return render_template("500_error.html"), 500


@app.context_processor
def get_status():
    db_session = DBSession(db.engine)
    status_list = [curr_status.value for curr_status in db_session.session.query(Status).order_by(Status.value).all()]
    status_url = [curr_status.strip("!").replace(" ", "_").lower() for curr_status in status_list]
    return dict(status_list=status_list, status_url=status_url)


@app.route("/", methods=("GET", ))
def index():
    return render_template("index.html")


@app.route("/about", methods=("GET", ))
def about():
    return render_template("about.html")


@app.route("/subscribe", methods=("GET", "POST"))
def subscribe():
    if request.method == "POST":
        user_mail = request.form.get('mail')
        if '@' in user_mail:
            db_session = DBSession(db.engine)
            user = User(mail=user_mail)
            msg = "Successful subscribed!" if db_session.add_user(user) else "Already subscribed!"
            return render_template("subscribe_info.html", msg=msg)
        else:
            return render_template("subscribe_info.html", msg="Invalid type of email, please check!")

    return render_template("subscribe.html")


@app.route("/<status_value>", methods=("GET", ))
def status(status_value: str):
    status_dict = get_status()
    status_list, status_url = status_dict["status_list"], status_dict["status_url"]

    if status_value in status_url:
        status_title = status_list[status_url.index(status_value)]
        db_session = DBSession(db.engine)
        db_status = db_session.session.query(Status).filter_by(value=status_title).first()
        query = db_session.session.query(PEP).filter_by(status_id=db_status.id)
        peps = query.all()
        return render_template("pep_info.html", status_title=status_title, peps=peps)
    else:
        return handle_404(status_value)
