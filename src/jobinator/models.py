from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker
import sqlalchemy.types as types
import sqlalchemy as sa
from horus.models import GroupMixin
from horus.models import UserMixin
from horus.models import UserGroupMixin
from horus.models import ActivationMixin
from horus.models import BaseModel
from zope.sqlalchemy.datamanager import ZopeTransactionExtension
from pyramid.i18n import TranslationStringFactory
from hem.db import get_session

import cjson as json
import operator

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base(cls=BaseModel)

_ = TranslationStringFactory('jobinator')

OPERATORS = ('==', '!=', '<', '>')
OPERATORS = map(lambda x: (x, x), OPERATORS)

FACT_TYPE_BOOL = 'bool'
FACT_TYPE_NUMBER = 'number'

FACT_TYPES = (FACT_TYPE_BOOL, FACT_TYPE_NUMBER)
FACT_TYPES = map(lambda x: (x, x), FACT_TYPES)

FACT_LIST = map(lambda x: (x, sa.Boolean, False), ('jQuery', 'Web', 'J2EE', 'Git', 'Java',
                    'RDBMS', 'NoSQL', 'Flask', 'JavaScript', 'Redis', 'CVS', 'Rails',
                    'Celery', 'GWT', '1C', 'PHP', 'MySQL', 'Jenkins', 'Riak', 'DVCS',
                    'Hibernate', 'Pylons', 'Tornado', 'AWS', 'PostGIS', 'Maven',
                    'CoffeeScript', 'Ajax', 'html', 'Ruby', 'SVN', 'Mercurial', 'DB',
                    'CouchDB', 'Django', 'Lucene', 'VCS', 'Cpp', 'SOLR', 'CSS', 'QT',
                    'Pyramid', 'PostgreSQL', 'Mongo', 'Spring', 'SQL', 'Rest', 'Python',
                    'Gevent', 'Linux', 'Widows', 'msSQL'
            )) + \
            map(lambda x: (x, sa.Integer, None), ('salary_from', 'salary_to'))


class ChoiceType(types.TypeDecorator):

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.iteritems() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


class JSONEncodedDict(types.TypeDecorator):
    """Represents an immutable structure as a json-encoded string.

    Usage::

        JSONEncodedDict()

    """

    impl = types.Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.encode(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.decode(value)
        return value


class ManagerMixin(object):
    """ Mixin with basic manager facility """

    @classmethod
    def get_all(cls, request, page=None, limit=None):
        """ Gets all records of the specific item with option page and
        limits
        """
        session = get_session(request)

        query = session.query(cls)

        if limit:
            query = query.limit(limit)

        if page and limit:
            offset = (page - 1) * limit
            query = query.offset(offset)

        return query

    @classmethod
    def get_by_pk(cls, request, pk):
        """Gets an object by its primary key"""
        session = get_session(request)

        return session.query(cls).filter(cls.pk == pk).first()


class User(UserMixin, Base):
    """ User """

    @property
    def __acl__(self):
        return super(User, self).__acl__ + [
                (Allow, 'user:%s' % self.pk, 'filter_list')
        ]


class Group(GroupMixin, Base):
    """ Group """


class UserGroup(UserGroupMixin, Base):
    """ User Group """


class Activation(ActivationMixin, Base):
    """ Registration Activation """


class ScrapedData(ManagerMixin, Base):
    """
    Scraped data storage.
    Model stores raw data from spiders.

    data - json object with fields: salary, city, title, contract (hours number|full time)
    """
    title = sa.Column(sa.Unicode(255), nullable=True)
    data = sa.Column(sa.Text, nullable=True)
    url = sa.Column(sa.Unicode(255), nullable=False)
    preview = sa.Column(sa.Text, nullable=True)

    __table_args__ = (
        sa.schema.UniqueConstraint("url",),
        )


class Setting(ManagerMixin, Base):
    """ Setting """

    key = sa.Column(sa.Unicode(255), nullable=False, index=True)
    value = sa.Column(sa.Unicode(255), nullable=True)


class Fact(ManagerMixin, Base):
    """ Fact """

    name = sa.Column(sa.Unicode(255), nullable=False, index=True)
    type = sa.Column(ChoiceType(FACT_TYPES), nullable=False, index=True)
    args = sa.Column(sa.Text, nullable=True)


class FactLinks(ManagerMixin, Base):
    """ Fact Links """
    name = sa.Column(sa.Unicode(255), nullable=False, index=True)
    args = sa.Column(sa.Text, nullable=True)


class FactData(ManagerMixin):

    def __init__(self, **kw):
        for k,v in kw.iteritems():
            setattr(self, k, v)

    @classmethod
    def fact_by_id(cls, id):
        return getattr(cls, FACT_LIST[id][0])


columns = [sa.Column(columnName, columnType(), default=default) for columnName, columnType, default in FACT_LIST]

factTable = sa.Table('fact_data', Base.metadata, sa.Column('pk', sa.Integer, primary_key=True),
                     sa.Column('scraped_data_id', sa.Integer, sa.ForeignKey(ScrapedData.pk)), *columns)

sa.orm.mapper(FactData, factTable, properties={
    'scraped_data' : sa.orm.relationship(ScrapedData, backref=sa.orm.backref("fact_data_items"))
})

#class FactData(ManagerMixin, Base):
#    """ Fact Data """
#
#    fact_id = sa.Column(sa.Integer, sa.ForeignKey(Fact.pk))
#
#    fact = sa.orm.relationship("Fact", backref=sa.orm.backref("fact_data"))
#
#    min = sa.Column(sa.Integer, nullable=True, index=True)
#    max = sa.Column(sa.Integer, nullable=True, index=True)
#    value = sa.Column(sa.Unicode(255), nullable=True, index=True)


class UserFilter(ManagerMixin, Base):
    """ User Filter """

    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.pk))

    user = sa.orm.relationship("User", backref=sa.orm.backref("filters"))

    name = sa.Column(sa.Unicode(255), nullable=False, index=True)

    filter_details = sa.Column(JSONEncodedDict(), nullable=False)

    def build_query(self, details=None):

        OPERATOR_MAP = {'All': sa.and_,
                        'Any': sa.or_}

        CONDITION_MAP = {'IsNull': lambda x: x == False,
                         'NotNull': lambda x: x == True,
                         'GreaterThan': lambda x, y: x > y,
                         'GreaterOrEqual': lambda x, y: x >= y,
                         'LessThan': lambda x, y: x < y,
                         'LessOrEqual': lambda x, y: x <= y,
                         }

        if details is None:
            details = self.filter_details
            if isinstance(details, basestring):
                details = json.decode(details)
            details = details['root']
            details['typeName'] = 'PDCT'
        if isinstance(details, dict) and details['typeName'] == 'PDCT' and details.get('enabled', False):
            operator = OPERATOR_MAP[details['linkType']]
            return operator(*self.build_query(details['conditions']))
        if isinstance(details, dict) and  details['typeName'] == 'SMPL' and  details.get('enabled', False):
            if details['operatorID'] in ['GreaterThan', 'GreaterOrEqual', 'LessThan', 'LessOrEqual']:
                return CONDITION_MAP[details['operatorID']](FactData.fact_by_id(details['expressions'][0]['id']),
                                                            details['expressions'][1]['value'])
            else:
                return CONDITION_MAP[details['operatorID']](FactData.fact_by_id(details['expressions'][0]['id']))
        conditions = []
        for detail in details:
            if detail['enabled']:
                conditions.append(self.build_query(detail))
        return conditions


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
