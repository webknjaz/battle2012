
from cStringIO import StringIO

from scrapy.exceptions import DropItem

from scrapy import log
from scrapy.contrib.exporter import JsonItemExporter
from scrapy.conf import settings
from sqlalchemy import exc

from jobinator.models import DBSession, ScrapedData
import transaction


class PostgresDBStorage(object):

    def process_item(self, item, spider):
        """ This method is called each time an item is scraped from a webpage.
        If the item validates, we store it in the PostgresDB collection. If not,
        we drop it.
        """
        # Validate vacancy
        if not item['url'] or not item.has_key("title"):
            raise DropItem("Missing job url")
        else:
            # If valid article, save it to SQAlchemy model
            # Log this insertion
            url = item["url"]
            del item["url"]
            if item.has_key("preview"):
                preview = item["preview"]
                del item["preview"]
            else:
                preview = ""
            exporter = JsonItemExporter(StringIO())
            exporter.export_item(item)

            item_object = ScrapedData(title = unicode(item["title"]), data = unicode(exporter.file.getvalue()),
                                      url = unicode(url), preview = unicode(preview))
            try:
                DBSession.add(item_object)
                transaction.commit()
                log.msg("Item wrote to Postgres database", level=log.DEBUG, spider=spider)
            except exc.IntegrityError:
                transaction.abort()
                raise DropItem("Duplicated url %s" % url)

        return item
