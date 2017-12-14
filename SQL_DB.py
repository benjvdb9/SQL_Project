from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Time

Base = declarative_base()

class Trajets(Base):
    __tablename__ = 'Trajets'
    id_trajets = Column(Integer, primary_key=True)
    heure_depart = Column(Time)
    gare_depart = Column(String(50))
    id_train = Column(Integer, ForeignKey('Train.id_train'))

    def getID():
        return 'id_trajets'

class Station(Base):
    __tablename__ = 'Station'
    nom = Column(String(50))
    id_station = Column(String(50), primary_key=True)

    def getID():
        return Station.id_station

class LienTrajetsStation(Base):
    __tablename__ = 'LienTrajetStation'
    id_trajets = Column(Integer, ForeignKey('Trajets.id_trajets'), primary_key=True)
    id_station = Column(Integer, ForeignKey('Station.id_station'), primary_key=True)
    decalage = Column(Integer)
    retard = Column(Integer)

    def getID(self):
        return 'Unknown'

class Train(Base):
    __tablename__ = 'Train'
    id_train = Column(Integer, primary_key=True)
    nb_wagon = Column(Integer)
    id_pc = Column(Integer, ForeignKey('PC.id_pc'))

    def getID():
        return Train.id_train

class PC(Base):
    __tablename__ = 'PC'
    id_pc = Column(Integer, primary_key=True)
    position_pc = Column(Integer)

    def getID():
        return 'id_pc'

class Utility():
    def __init__(self):
        self.session = self.createSession()
    
    def createSession(self):
        engine = create_engine('sqlite:///train_alchemy.db')
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        return session

    def addTrainTest(self):
        new_train = Train(id_train= 99, nb_wagon= 10, id_pc= 1)
        self.session.add(new_train)
        self.session.commit()

    def eraseTrainTest(self):
        self.session.query(Train).filter(Train.id_train == 99).delete()
        self.session.commit()
