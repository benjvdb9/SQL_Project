import SQL_DB
from datetime import timedelta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class DB_Manager():
    def __init__(self):
        self.engine  = ''
        self.session = self.createSession()
        self.list_cache = []

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

    def printResult(self, result, structure, *args):
        print_ttl = []
        for row in result:
            timesum = row[1] + timedelta(minutes = row[6])
            printstr= structure.format(*self.list_decorator(row, timesum, *args))
            print_ttl.append(printstr)
        return print_ttl

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
        self.printList(self.printResult(result, '{}, {} +{}', 9, 'HM', 8))

    def getTrainInfo(self, id_tr):
        s = select([SQL_DB.Trajets, SQL_DB.Train, SQL_DB.PC]).\
            where(SQL_DB.Trajets.id_train == SQL_DB.Train.id_train).\
            where(SQL_DB.Train.id_pc == SQL_DB.PC.id_pc)

        s = s.where(SQL_DB.Trajets.id_trajets == id_tr)
        result = self.applySQL(s)

        self.list_cache = []
        print_rst = self.printResult(
            result, 'Nombe de wagons: {}\nWagons première classe: {}', 6, [10])
        print(print_rst[-1])

    def getStationInfo(self, id_st):
        s = self.getMergedTable()

        id_st = self.getStationID(id_st)
        s = s.where(SQL_DB.Station.id_station == id_st)

        result = self.applySQL(s)
        self.printList(
            self.printResult(result, '{}, {} +{} -> {}', 9, 'HM', 8, 4))

    def getStationID(self, st_name):
        s = select([SQL_DB.Station]).\
            where(SQL_DB.Station.nom == st_name)

        result = self.applySQL(s).first()
        if result == None:
            return st_name
        else:
            return result[1]

    def list_decorator(self, row, timesum, *args):
        i = 0
        args = list(args)
        for elem in args:
            if type(elem) == int:
                args[i] = str(row[elem])
            elif type(elem)  == list:
                self.list_cache.append(row[elem[0]])
                args[i] = str(self.list_cache)
            elif elem == 'HM':
                args[i] = str(timesum.strftime("%H:%M"))
            else:
                args[i] = elem
            i+=1
        return tuple(args)

    def printList(self, lst):
        for elem in lst:
            print(elem)

    def reset(self):
        input('Reseting DB, continue?')
        self.session.query(SQL_DB.Trajets).delete()
        self.session.query(SQL_DB.Station).delete()
        self.session.query(SQL_DB.LienTrajetsStation).delete()
        self.session.query(SQL_DB.Train).delete()
        self.session.query(SQL_DB.PC).delete()
        self.session.commit()
