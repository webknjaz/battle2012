# -*- coding: utf-8 -*-

facts = dict(
    #python
    Python=['python', u'питон', u'пайтон'],
    Django=['django', u'джанго', u'жанго'],
    Gevent=['gevent'],
    Tornado=['tornado'],
    Flask=['flask'],
    Celery=['celery'],
    Pylons=['pylons'],
    Pyramid=['pyramid'],

    # languages
    Java = ['java'],
    J2EE = ['j2ee', u'j2ее', 'java entrprise edition'],
    Hibernate = ['hibernate', u'хибер'],
    Spring = ['spring', u'спринг'],
    Maven = ['maven', u'мэйвен', u'мейвен'],
    GWT = ['gwt', u'гвт', u'жвт'],
    Cpp = ['c++', u'с++'],
    PHP = ['php', u'рнр', u'пхп'],
    QT = ['qt'],
    Ruby = ['ruby', u'руби'],
    Rails = ['rails', u'рэйлс', u'рейлс'],

    # database
    PostgreSQL=['postgre', 'posgre'],
    SQL=['sql'],
    MySQL=['mysql', u'мускуль'],
    msSQL=['mssql'],
    NoSQL=['nosql', 'no sql'],
    Mongo=['mongo', u'монго'],
    CouchDB=['couchdb', u'коуч', u'кауч'],
    Redis=['redis', u'редис'],
    Riak=['riak'],
    SOLR=['solr'],
    Lucene=['lucene'],
    PostGIS=['postgis'],

    # web
    jQuery=['jquery'],
    html=['html'],
    CSS=['css'],
    JavaScript=['js', 'javascript', u'жаваскрипт'],
    CoffeeScript=['coffeescript'],
    Ajax=['ajax'],
    Rest=['rest'],

    # os
    Linux=['linux'],
    Widows=['win'],

    # control versions
    Git = ['git', u'гит'],
    Mercurial = ['mercurial', 'hg', u'меркуриал'],
    SVN = ['svn'],
    CVS = ['cvs'],
    Jenkins = ['jenkins'],

    # cloud
    AWS=['aws', 'amazonwebservices', 'ec2', 's3']

    # other
)

# other
facts['1C'] = ['1c', u'1с']

factLinks = dict(
    Python = ['Django', 'Tornado', 'Pylons', 'Pyramid', 'Flask', 'Gevent', 'Celery'],
    Web = ['jQuery', 'html', 'CSS', 'JavaScript', 'CoffeeScript', 'Ajax', 'Rest', 'Django', 'Tornado', 'Pylons', 'Pyramid', 'Flask', 'Rails'],
    DVCS = ['Git', 'Mercurial'],
    VCS = ['DVCS', 'SVN', 'CVS'],
    RDBMS = ['PostgreSQL', 'MySQL', 'msSQL', 'PostGIS', 'SQL'],
    NoSQL = ['Mongo', 'NoSQL', 'CouchDB', 'Redis', 'Riak', 'SOLR', 'Lucene'],
    DB = ['RDBMS', 'NoSQL'],
    Java = ['J2EE', 'GWT'],
    J2EE = ['Hibernate', 'Spring', 'Maven'],
    Ruby = ['Rails'],
)

unique = set(facts.keys())
unique.update(factLinks.keys())