from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class HostedGame(Base):
    __tablename__ = "hosted_games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    startDate = Column(DateTime)
    isActive = Column(Boolean)
    host = Column(String(36), ForeignKey("users.id"))

    host_user = relationship("User", back_populates="hosted_games")