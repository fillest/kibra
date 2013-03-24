from sqlalchemy.orm import relationship
from . import DBObject, DBSession, QueryPropMixin


class Entry (DBObject, QueryPropMixin):
    __tablename__ = 'entries'

    tags = relationship('Tag',
        secondary = 'entries__tags',
        order_by = 'Tag.name.asc()',
        passive_deletes = True,
    )

    def __repr__ (self):
        return '<%s.%s #%s>' % (self.__class__.__module__, self.__class__.__name__, self.id)


class Tag (DBObject, QueryPropMixin):
    __tablename__ = 'tags'

    def __repr__ (self):
        return "<%s.%s #%s '%s'>" % (self.__class__.__module__, self.__class__.__name__, self.id, self.name)
