from sqlalchemy import Column, Integer, String
from database import Base


class Sensor(Base):
    __tablename__ = 'sensores'
    id = Column(Integer, primary_key=True)
    regiao = Column(String(10))
    timestamp = Column(String(20))
    tag = Column(String(45))
    valor = Column(String(10))
    status = Column(String(10))

    def as_dict(self):
        return {item.name: getattr(self, item.name) for item in self.__table__.columns}
