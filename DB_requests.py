import SQL_DB
from datetime import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class DB_Manager():
    def __init__(self):
        self.session = self.createSession()

    def createSession(self):
        Base = declarative_base()
        engine = create_engine('sqlite:///train_alchemy.db')
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        return session
    
    def addToTable(self, table, **kwargs):
        new_object = table(**kwargs)
        self.session.add(new_object)
        self.session.commit()

    def removeFromTable(self, table, id):
        self.session.query(table).filter(table.getID() == id).delete()
        self.session.commit()


dbm = DB_Manager()
#dbm.addToTable(SQL_DB.Train, id_train = 1, nb_wagon = 2, id_pc = 3)
#dbm.removeFromTable(SQL_DB.Train, 1)

#Le trajet Ottignies-Schuman
'''dbm.addToTable(SQL_DB.Trajets, id_trajets= 1, heure_depart= time(6, 45),
               gare_depart= 'Ottignies', id_train= 30)'''

#Toutes les stations desservies
'''dbm.addToTable(SQL_DB.LienTrajetsStation, id_trajets= 30, id_station= 6,
               decalage= 0, retard= 5)
dbm.addToTable(SQL_DB.LienTrajetsStation, id_trajets= 30, id_station= 7,
               decalage= 10, retard= 5)
dbm.addToTable(SQL_DB.LienTrajetsStation, id_trajets= 30, id_station= 8,
               decalage= 20, retard= 0)
dbm.addToTable(SQL_DB.LienTrajetsStation, id_trajets= 30, id_station= 9,
               decalage= 30, retard= 0)'''

#La db des stations
dbm.addToTable(SQL_DB.Station, nom= 'Ottignies', id_station= 6)
dbm.addToTable(SQL_DB.Station, nom= 'Etterbeek', id_station= 7)
dbm.addToTable(SQL_DB.Station, nom= 'Bxl-Luxembourg', id_station= 8)
dbm.addToTable(SQL_DB.Station, nom= 'Bxl-Schuman', id_station= 9)
