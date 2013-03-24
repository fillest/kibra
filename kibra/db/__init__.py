import logging
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension


log = logging.getLogger(__name__)
DBSession = scoped_session(sessionmaker(extension = ZopeTransactionExtension()))
DBObject = declarative_base()


def init (engine):
    DBSession.configure(bind = engine)
    DBObject.metadata.bind = engine
    
    with set_db_log_level(logging.WARN):
        DBObject.metadata.reflect()


def get_db_session ():
    # dont pass params that differ from scoped session here
    # like expire_on_commit=False, you will get errors like
    # 'scoped session already exists' in a strange way (not instantly).
    # seems, new scoped session is being created if params differ
    return DBSession()


@contextmanager
def set_db_log_level (level):
    db_logger = logging.getLogger('sqlalchemy.engine')
    old_level = db_logger.level
    db_logger.level = level
    
    try:
        yield
    finally:
        db_logger.level = old_level


class QueryPropMixin (object):
    q = DBSession.query_property()