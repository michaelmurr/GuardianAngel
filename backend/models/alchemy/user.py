import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey,Float, Table
from database import Base
from sqlalchemy.orm import relationship


friendship = Table(
    'friendship', Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id'), primary_key=True),
    Column('friend_id', String(36), ForeignKey('users.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    picture = Column(String)
    street = Column(String)
    city = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    hashed_password = Column(String)

    friends = relationship(
        'User',
        secondary=friendship,
        primaryjoin=id == friendship.c.user_id,
        secondaryjoin=id == friendship.c.friend_id,
        backref='friends_back'
    )

    def all_friends(self):
        return list(set(self.friends + self.friends_back))  


