from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base


class Count(Base):
    __tablename__ = 'Count'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    count = Column(Integer)
    topic = Column(Text)



