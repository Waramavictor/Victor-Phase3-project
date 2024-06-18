
from sqlalchemy import Boolean
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_time = Column(DateTime)
    cancelled = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Appointment(name='{self.name}', date_time='{self.date_time}', cancelled={self.cancelled})>"

class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer)
    vote = Column(Integer)  # 1 for yes, 0 for no

    def __repr__(self):
        return f"<Vote(appointment_id={self.appointment_id}, vote={self.vote})>"