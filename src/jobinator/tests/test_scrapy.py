import unittest
from pyramid import testing
from jobinator.models import ScrapedData
from jobinator.tests.base import BaseTestCase


class ScrapedDataModelTest(BaseTestCase):

    def test_scrapied_data_model(self):
        item = ScrapedData(title='test job', data='test data', url="http://example.com", preview = "test preview")
        self.session.add(item)
        self.session.flush()

        assert item.title == 'test job'
        assert item.data == 'test data'
        assert item.url == "http://example.com"
        assert item.preview == "test preview"
