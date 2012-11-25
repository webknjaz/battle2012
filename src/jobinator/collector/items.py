# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CollectorItem(Item):
    # define the fields for your item here like:
    title = Field(serializer=str)
    company = Field(serializer=str)
    salary = Field(serializer=str)
    contract = Field(serializer=str)
    region = Field(serializer=str)
    url = Field(serializer=str)
    experience = Field(serializer=str)
    description = Field(serializer=str)
    preview = Field(serializer=str)
    keys = Field(serializer=str)

