import SQL_DB
from datetime import timedelta
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
        import pdb; pdb.set_trace()
        for row in result:
            timesum = row[1] + timedelta(minutes = row[3])
            printstr = row[2] + ', ' + str(timesum.strftime("%H%M"))
            print(printstr)

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
        self.printResult(result)

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
