from sqlalchemy import Column, String, Float, Integer, Text, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.username")) 

    start_latitude = Column(Float)
    start_longitude = Column(Float)
    end_latitude = Column(Float)
    end_longitude = Column(Float)

    start_address = Column(String)
    end_address = Column(String)
    polyline = Column(Text)  

    user = relationship("User", back_populates="routes")