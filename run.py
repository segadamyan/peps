from scripts import PEPScrap, DBSession, Mail
from app import app
from models import Database
from apscheduler.schedulers.background import BackgroundScheduler
import os


def db_integration():
    peps = PEPScrap("https://www.python.org/dev/peps/").data_pep()
    db = Database() if os.path.abspath(os.getcwd()).endswith("app") else Database("app")
    db.create_db()
    db_session = DBSession(db.engine)
    new_peps = []
    for pep in peps:
        if db_session.add_pep(pep):
            new_peps.append(pep)

    users = db_session.get_users()
    mail = Mail("pep.project2021@gmail.com", "acapep2021")
    mail.send_info(users, new_peps)


if __name__ == "__main__":
    if not (os.path.exists("pep.db") or os.path.exists(os.path.join("app", "pep.db"))):
        db_integration()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=db_integration, trigger="interval", weeks=1)
    scheduler.start()
    app.app.run()
