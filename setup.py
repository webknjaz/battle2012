import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'setuptools',
    'pyramid',
    'pycrypto',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_rpc',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'Paste',
    'alembic',
    'horus',
    'webtest',
    'mock',
    'hiero',
    'python-cjson',
    'webhelpers'
    ]

setup(name='jobinator',
      version='0.0',
      description='jobinator',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Jobinator Team',
      author_email='team@jobinator.org.ua',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages('src'),
      package_dir={'':'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""\
      [console_scripts]
      factorize = jobinator.facts.start:start
      upload_facts = jobinator.facts.start:uploadFacts

      [paste.app_factory]
      main = jobinator:main
      """,
      )

