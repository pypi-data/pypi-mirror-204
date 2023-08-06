from os import mkdir, path
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from investing_algorithm_framework.domain import SQLALCHEMY_DATABASE_URI, \
    OperationalException, DATABASE_NAME, DATABASE_DIRECTORY_PATH

Session = sessionmaker()
logger = logging.getLogger(__name__)


class SQLAlchemyAdapter:

    def __init__(self, app):

        if SQLALCHEMY_DATABASE_URI not in app.config \
                or app.config[SQLALCHEMY_DATABASE_URI] is None:
            raise OperationalException("SQLALCHEMY_DATABASE_URI not set")

        if not app.stateless:
            database_dir = app.config[DATABASE_DIRECTORY_PATH]
            database_name = app.config[DATABASE_NAME]
            database_path = path.join(database_dir, database_name)

            if not path.exists(database_dir):
                try:
                    mkdir(database_dir)
                    open(database_path, 'w').close()
                except OSError as e:
                    logger.error(e)
                    raise OperationalException(
                        "Could not create database directory"
                    )

        global Session
        engine = create_engine(app.config[SQLALCHEMY_DATABASE_URI])
        Session.configure(bind=engine)


def setup_sqlalchemy(app, throw_exception_if_not_set=True):

    try:
        SQLAlchemyAdapter(app)
    except OperationalException as e:
        if throw_exception_if_not_set:
            raise e

    return app


class SQLBaseModel(DeclarativeBase):
    pass


def create_all_tables():
    SQLBaseModel.metadata.create_all(bind=Session().bind)
