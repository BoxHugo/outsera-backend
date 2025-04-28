from sqlalchemy import Column, Integer, String
from app.infra.db.session import BASE


class StudioDB(BASE):
    __tablename__ = "studios"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
