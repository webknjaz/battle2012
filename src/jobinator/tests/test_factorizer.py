import unittest
from pyramid import testing
from jobinator.models import Setting, Fact, FactData, FACT_TYPE_BOOL, ScrapedData
from jobinator.tests.base import BaseTestCase


class SettingModelTest(BaseTestCase):

    def test_settings_model(self):
        item = Setting(key='key', value='value')
        self.session.add(item)
        self.session.flush()

        assert item.key == 'key'
        assert item.value == 'value'


class FactModelTest(BaseTestCase):

    def test_fact_model(self):
        item = Fact(name='name', type=FACT_TYPE_BOOL, args='args')
        self.session.add(item)
        self.session.flush()

        assert item.name == 'name'
        assert item.type == FACT_TYPE_BOOL
        assert item.args == 'args'

class FactDataModelTest(BaseTestCase):

    def test_fact_data_model(self):
        data = ScrapedData(url='http://some.com')
        item = FactData(html=True, scraped_data=data)
        self.session.add(item)
        self.session.flush()

        assert item.html == True
        assert item.scraped_data == data

