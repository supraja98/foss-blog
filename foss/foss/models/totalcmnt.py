from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base


class Total(Base):
    __tablename__ = 'Total'
    name = Column(Text , primary_key=True)
    tot = Column(Integer)

