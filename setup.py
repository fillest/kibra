import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
#CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()


requires = [
    'pyramid==1.1',
    'SQLAlchemy==0.7',
    'Mako==0.4.2',
    'transaction',
    'repoze.tm2==1.0b1',  # default_commit_veto
    'zope.sqlalchemy',
    'WebError',
    'psycopg2',
    # 'ipython==0.10',  # pyramid==1.1 doesnt work with ipython==0.11
    'webhelpers==1.3',
    'WTForms==0.6.3',
    'fabric==1.2',
    'gunicorn',
    'setproctitle',  # for gunicorm
]

setup(name='kibra',
      version='0.1',
      description='kibra',
#      long_description=README + '\n\n' +  CHANGES,
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='f',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='kibra',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = kibra:main
      """,
      paster_plugins=['pyramid'],
      )

