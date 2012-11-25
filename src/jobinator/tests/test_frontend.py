import unittest
from pyramid import testing
from jobinator.models import User, UserFilter, Fact, FACT_TYPE_BOOL, ScrapedData, FactData
from jobinator.tests.base import BaseTestCase
from sqlalchemy.orm.query import Query
import sqlalchemy as sa

class UserFilterTest(BaseTestCase):

    def test_user_filter_model(self):

        filter_details={"root":{"linkType":"All",
                                  "enabled":True,
                                  "conditions":[{"justAdded":False,
                                                 "typeName":"SMPL",
                                                 "enabled":True,
                                                 "operatorID":"NotNull",
                                                 "expressions":[{"typeName":"ENTATTR",
                                                                 "id":0}]},
                                                {"justAdded":False,
                                                 "typeName":"SMPL",
                                                 "enabled":True,
                                                 "operatorID":"IsNull",
                                                 "expressions":[{"typeName":"ENTATTR",
                                                                 "id":1}]},
                                                {"typeName":"PDCT",
                                                 "linkType":"Any",
                                                 "enabled": True,
                                                 "conditions":[
                                                               {"justAdded":False,
                                                                 "typeName":"SMPL",
                                                                 "enabled":True,
                                                                 "operatorID":"NotNull",
                                                                 "expressions":[{"typeName":"ENTATTR",
                                                                                 "id":3}]},
                                                                {"justAdded":False,
                                                                 "typeName":"SMPL",
                                                                 "enabled":True,
                                                                 "operatorID":"IsNull",
                                                                 "expressions":[{"typeName":"ENTATTR",
                                                                                 "id":4}]},
                                                               ]}]},
                                  "columns":[],
                                  "justsorted":[]}

        user = User(user_name='user', password='password', salt='salt', email='test@some.com')
        item = UserFilter(user=user, name='name', filter_details=filter_details)
        self.session.add(item)
        self.session.flush()

        assert item.user == user
        assert item.name == 'name'
        assert item.filter_details == filter_details

        assert str(item.build_query()) == str(sa.and_(FactData.fact_by_id(0) == True,
                                      FactData.fact_by_id(1) == False,
                                      sa.or_(FactData.fact_by_id(3) == True,
                                          FactData.fact_by_id(4) == False)
                                      ))
