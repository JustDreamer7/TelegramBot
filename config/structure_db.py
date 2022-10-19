from sqlalchemy import Column, Integer, DateTime, Text, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(Text)
    registration_date = Column(DateTime)


class Messages(Base):
    __tablename__ = "messages"
    message_id = Column(Integer, primary_key=True)
    message_text = Column(Text)
    sender = Column(Text)
    sending_time = Column(DateTime)
    has_location = Column(Boolean)
    has_contact = Column(Boolean)
