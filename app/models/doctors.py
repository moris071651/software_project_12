from sqlalchemy import Column, Integer, String

from app.models import Base


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    address = Column(String)
    password = Column(String)
