from scripts import PEPScrap, DBSession
from models import Database
import schedule


def run_app():
    peps = PEPScrap("https://www.python.org/dev/peps/").data_pep()
    db = Database("app")
    db.create_db()
    db_session = DBSession(db.engine)
    for pep in peps:
        db_session.add_pep(pep)


if __name__ == "__main__":
    run_app()
    schedule.every().monday.at("12:00").do(run_app)
    while True:
        schedule.run_pending()
