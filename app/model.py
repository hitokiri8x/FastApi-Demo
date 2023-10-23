from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DECIMAL, Float
from sqlalchemy.orm import sessionmaker, relationship, Mapped
from sqlalchemy.engine import create_engine

engine = create_engine('sqlite:///app/cdatabase.s3db')
Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    info: Mapped[List["Info"]] = relationship("Info")

    def __init__(self, name, type, address):
        self.name = name
        self.type = type
        self.address = address


class Info(Base):
    __tablename__ = 'info'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    voto_medio = Column(DECIMAL, nullable=True)
    tipo_piatto_principale = Column(String(255), nullable=True)
    prezzo_piatto_principale = Column(DECIMAL, nullable=True)
    voto_piatto_principale = Column(DECIMAL, nullable=True)
    distanza_dal_centro = Column(Float, nullable=True)
    restaurant: Mapped["Restaurant"] = relationship(back_populates="info")

    def __init__(self, restaurantid, voto_medio, tipo_piatto_principale, prezzo_piatto_principale,
                 voto_piatto_principale, distanza_dal_centro):
        self.restaurant_id = restaurantid
        self.voto_medio = voto_medio
        self.tipo_piatto_principale = tipo_piatto_principale
        self.prezzo_piatto_principale = prezzo_piatto_principale
        self.voto_piatto_principale = voto_piatto_principale
        self.distanza_dal_centro = distanza_dal_centro


def add_restaurant(session, name, type, address, info=None):
    temp = Restaurant(name=name, type=type, address=address)
    session.add(temp)
    session.flush()
    if info:
        temp2 = Info(restaurantid=temp.id, voto_medio=info.voto_medio,
                       tipo_piatto_principale=info.tipo_piatto_principale,
                       prezzo_piatto_principale=info.prezzo_piatto_principale,
                       voto_piatto_principale=info.voto_piatto_principale,
                       distanza_dal_centro=info.distanza_dal_centro)
        session.add(temp2)
    session.commit()


def get_all_restaurants(session):
    result = session.query(Restaurant).all()
    return result


try:
    Base.metadata.create_all(engine)
except Exception as e:
    print(e)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

