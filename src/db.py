from sqlmodel import SQLModel, create_engine, Session


class Engine:
    __url = ""
    __engine = None

    @classmethod
    def load(cls, driver, user, password, host, port, dbname):
        cls.__url = f"postgresql+{driver}://{user}:{password}@{host}:{port}/{dbname}"

    @classmethod
    def get_engine(cls):
        if not cls.__engine:
            cls.__engine = create_engine(cls.__url)
        return cls.__engine

    @classmethod
    def create_new_tables(cls):
        engine = cls.get_engine()
        SQLModel.metadata.create_all(engine)

    @classmethod
    def get_session(cls):
        return Session(cls.get_engine())
