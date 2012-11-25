from pyramid.compat import configparser
from sqlalchemy import engine_from_config

from jobinator.models import DBSession, initialize_sql
from ConfigParser import InterpolationMissingOptionError


def load_config(filename='development.ini', basePath='.'):
    config = load_settings(filename, basePath)

    engine = engine_from_config(config, 'sqlalchemy.')

    DBSession.configure(bind=engine)

    initialize_sql(engine)


##In your worker
#DBSession.add(<model instance>)

def load_settings(configurationPath, basePath):
    'Load sensitive settings from hidden configuration file'
    settings = {}
    defaultByKey = {'here': basePath}
    configParser  = configparser.ConfigParser(defaultByKey)
    if not configParser.read(configurationPath):
        raise Exception('Could not open %s' % configurationPath)
    for section in configParser.sections():
        try:
            settings.update(configParser.items(section))
        except InterpolationMissingOptionError:
            pass
    return settings
