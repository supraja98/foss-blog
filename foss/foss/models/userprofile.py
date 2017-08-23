from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base


class User(Base):
    __tablename__ = 'user'
    username = Column(Text, primary_key=True)
    password = Column(Text)


