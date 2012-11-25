# Scrapy settings for collector project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'collector'

SPIDER_MODULES = ['jobinator.collector.spiders']
NEWSPIDER_MODULE = 'jobinator.collector.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
#USER_AGENT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

ITEM_PIPELINES = [
    'jobinator.collector.pipelines.PostgresDBStorage',
    ]

CRAWL_LIMIT = 200

DOWNLOAD_DELAY = 0.3 # 1 second delay

COOKIES_ENABLED = True

#from pyramid.compat import configparser

from jobinator.config import load_config

load_config()