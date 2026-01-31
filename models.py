from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    destination = Column(String)

    activities = relationship("Activity", back_populates="trip")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date = Column(Date)
    location = Column(String)
    price=Column(Numeric(10, 2))
    trip_id = Column(Integer, ForeignKey("trips.id"))
    trip = relationship("Trip", back_populates="activities")