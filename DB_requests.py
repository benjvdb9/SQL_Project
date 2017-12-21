import SQL_DB
from datetime import time
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class DB_Manager():
    def __init__(self):
        self.engine  = ''
        self.session = self.createSession()

    def createSession(self):
        #Can be used to use the .db file but not to create a new one
        #or to update the structure of the database
        
        Base = declarative_base()
        self.engine = create_engine('sqlite:///train_alchemy.db')
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        return session
    
    def addToTable(self, table, **kwargs):
        new_object = table(**kwargs)
        self.session.add(new_object)
        self.session.commit()

    def removeFromTable(self, table, id):
        self.session.query(table).filter(table.getID() == id).delete()
        self.session.commit()

    def applySQL(self, SQL):
        conn = self.engine.connect()
        result = conn.execute(SQL)
        return result

    def printResult(self, result):
        for row in result:
            print(row)

    def getMergedTable(self):
        s = select([SQL_DB.Trajets, SQL_DB.LienTrajetsStation, SQL_DB.Station]).\
            where(SQL_DB.Trajets.id_trajets == SQL_DB.LienTrajetsStation.id_trajets).\
            where(SQL_DB.LienTrajetsStation.id_station == SQL_DB.Station.id_station)

        return s
            
    def selectTrajets(self, id_tr):
        s = self.getMergedTable()
        
        s = s.where(SQL_DB.Trajets.id_trajets == id_tr).\
            group_by(SQL_DB.LienTrajetsStation.decalage)
        
        result = self.applySQL(s)
        return result

    def getStationInfo(self, id_st):
        s = self.getMergedTable()

        s = s.where(SQL_DB.Station.id_station == id_st)

        result = self.applySQL(s)
        self.printResult(result)

    def reset(self):
        input('Reseting DB, continue?')
        self.session.query(SQL_DB.Trajets).delete()
        self.session.query(SQL_DB.Station).delete()
        self.session.query(SQL_DB.LienTrajetsStation).delete()
        self.session.query(SQL_DB.Train).delete()
        self.session.query(SQL_DB.PC).delete()
        self.session.commit()


#dbm = DB_Manager()
#dbm.addToTable(SQL_DB.Train, id_train = 1, nb_wagon = 2, id_pc = 3)
#dbm.addToTable(SQL_DB.PC, id_pc = 3, position_pc = 3)
#dbm.addToTable(SQL_DB.PC, id_pc = 3, position_pc = 6)
#dbm.addToTable(SQL_DB.PC, id_pc = 3, position_pc = 9)
#dbm.removeFromTable(SQL_DB.Train, 1)

#dbm.reset()

'''test = dbm.selectTrajets(1)
for elem in test:
    print(elem)
#dbm.getStationInfo(9)'''

#Le trajet Ottignies-Schuman
'''dbm.addToTable(SQL_DB.Trajets, id_trajets= 1, heure_depart= time(6, 45),
               gare_depart= 'Ottignies', id_train= 30)

#Toutes les stations desservies
dbm.addToTable(SQL_DB.LienTrajetsStation, id_trajets= 1, id_station= 6,
               decalage= 0, retard= 5)
dbm.addToTable(SQL_DB.LienTrajetsStation, id_trajets= 1, id_station= 7,
               decalage= 10, retard= 5)
dbm.addToTable(SQL_DB.LienTrajetsStation, id_trajets= 1, id_station= 8,
               decalage= 20, retard= 0)
dbm.addToTable(SQL_DB.LienTrajetsStation, id_trajets= 1, id_station= 9,
               decalage= 30, retard= 0)

#La db des stations
dbm.addToTable(SQL_DB.Station, nom= 'Ottignies', id_station= 6)
dbm.addToTable(SQL_DB.Station, nom= 'Etterbeek', id_station= 7)
dbm.addToTable(SQL_DB.Station, nom= 'Bxl-Luxembourg', id_station= 8)
dbm.addToTable(SQL_DB.Station, nom= 'Bxl-Schuman', id_station= 9)

#La db des trains
dbm.addToTable(SQL_DB.Train, id_train= 30, nb_wagon= 10, id_pc= 3)
dbm.addToTable(SQL_DB.Train, id_train= 31, nb_wagon= 10, id_pc= 3)'''
