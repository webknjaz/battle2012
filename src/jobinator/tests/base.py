import unittest
from pyramid import testing
from paste.deploy.loadwsgi import appconfig

from webtest import TestApp
from mock import Mock

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from jobinator.models import DBSession, initialize_sql
from jobinator.models import Base  # base declarative object
from jobinator import main
import os
here = os.path.dirname(__file__)
settings = appconfig('config:' + os.path.join(here, 'test.ini'))


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            os.unlink(os.path.join(here, 'test.db'))
        except (IOError, OSError):
            pass
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
        initialize_sql(cls.engine)
        cls.Session = sessionmaker()

    def setUp(self):
        connection = self.engine.connect()

        # begin a non-ORM transaction
        self.trans = connection.begin()

        # bind an individual Session to the connection
        DBSession.configure(bind=connection)
        self.session = self.Session(bind=connection)
        Base.session = self.session

    def tearDown(self):
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        testing.tearDown()
        self.trans.rollback()
        self.session.close()
