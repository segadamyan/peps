from flask import (
    Flask,
    url_for,
    render_template,
    request
)
from scripts import DBSession
from models import Database, PEP, Status

app = Flask(__name__)


@app.errorhandler(404)
def handle_404(err):
    return render_template("404_error.html", url=request.path), 404


@app.errorhandler(500)
def handle_500(err):
    return render_template("500_error.html"), 500


@app.context_processor
def get_status():
    db = Database()
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


@app.route("/<status_value>", methods=("GET", ))
def status(status_value: str):
    status_dict = get_status()
    status_list, status_url = status_dict["status_list"], status_dict["status_url"]

    if status_value in status_url:
        status_title = status_list[status_url.index(status_value)]
        db = Database()
        db_session = DBSession(db.engine)
        status_db = db_session.session.query(Status).filter_by(value=status_title).first()
        query = db_session.session.query(PEP).filter_by(status_id=status_db.id)
        peps = query.all()
        return render_template("pep_info.html", status_title=status_title, peps=peps)
    else:
        return handle_404(status_value)


if __name__ == '__main__':
    app.run(debug=True)
