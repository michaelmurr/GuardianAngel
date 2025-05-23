import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey,Float, Table
from database import Base
from sqlalchemy.orm import relationship


friendship = Table(
    'friendship', Base.metadata,
    Column('user_id', String, ForeignKey('users.username'), primary_key=True),
    Column('friend_id', String, ForeignKey('users.username'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'

 
    username = Column(String, unique=True,primary_key=True, index=True)
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
        primaryjoin=username == friendship.c.user_id,
        secondaryjoin=username == friendship.c.friend_id,
        backref='friends_back'
    )


    routes = relationship("Route", back_populates="user")
    
    def all_friends(self):
        return list(set(self.friends + self.friends_back))  

