from models import PEP, Status, Author
from sqlalchemy.orm import sessionmaker


class DBSession:
    def __init__(self, db_engine):
        self.session = sessionmaker(bind=db_engine)()

    def __add_status(self, status_value: str):
        query = self.session.query(Status).filter_by(value=status_value)
        exist_status = query.first()
        if exist_status is None:
            self.session.add(Status(value=status_value))

    def __get_status(self, status_value: str):
        query = self.session.query(Status).filter_by(value=status_value)
        exist_status = query.first()
        return exist_status

    def __check_existing_pep(self, pep_id):
        query = self.session.query(PEP).filter_by(pep=pep_id)
        return query.first()

    def __add_authors(self, current_pep: PEP, pep_info: dict):
        authors = [x.strip("\n").strip() for x in pep_info["Author"].split(",")]
        for author in authors:
            query = self.session.query(Author).filter_by(name=author)
            if query.first():
                pep_author = query.first()
            else:
                pep_author = Author(name=author)
            current_pep.authors.append(pep_author)

    def add_pep(self, pep_info: dict):
        exist_pep = self.__check_existing_pep(pep_info["PEP"])
        self.__add_status(pep_info["Status"])

        if exist_pep:
            exist_pep.status = pep_info["Status"]
            exist_pep.title = pep_info["Title"]
            exist_pep.type = pep_info["Type"]
            exist_pep.created = pep_info["Created"]
            exist_pep.authors = []
        else:
            exist_pep = PEP(
                pep=pep_info["PEP"],
                status_id=self.__get_status(pep_info["Status"]).id,
                title=pep_info["Title"],
                type=pep_info["Type"],
                created=pep_info["Created"]
            )
            self.session.add(exist_pep)

        self.__add_authors(exist_pep, pep_info)
        self.session.commit()
