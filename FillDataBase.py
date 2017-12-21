import SQL_DB
from datetime import time
from DB_requests import DB_Manager

class Filler():
    def __init__(self):
        self.Manager = DB_Manager()

    def reconnect(self):
        self.Manager = DB_Manager()

    def createDB(self):
        utils = SQL_DB.Utility()
        utils.createSession()

    def fillTrain(self):
        self.Manager.addToTable(SQL_DB.Train, id_train= 30, nb_wagon= 10, id_pc= 3)
        self.Manager.addToTable(SQL_DB.Train, id_train= 31, nb_wagon= 10, id_pc= 3)

    def fillPC(self):
        self.Manager.addToTable(SQL_DB.PC, id_pc = 3, position_pc = 3)
        self.Manager.addToTable(SQL_DB.PC, id_pc = 3, position_pc = 6)
        self.Manager.addToTable(SQL_DB.PC, id_pc = 3, position_pc = 9)

    def fillTrajets(self):
        self.Manager.addToTable(SQL_DB.Trajets, id_trajets= 1, heure_depart= time(6, 45),
               gare_depart= 'Ottignies', id_train= 30)
        self.Manager.addToTable(SQL_DB.Trajets, id_trajets= 2, heure_depart= time(6, 45),
               gare_depart= 'Ottignies', id_train= 31)

    def fillLienTrajetsStation(self):
        self.Manager.addToTable(SQL_DB.LienTrajetsStation, id_trajets= 1, id_station= 6,
               decalage= 0, retard= 5)
        self.Manager.addToTable(SQL_DB.LienTrajetsStation, id_trajets= 1, id_station= 7,
               decalage= 10, retard= 5)
        self.Manager.addToTable(SQL_DB.LienTrajetsStation, id_trajets= 1, id_station= 8,
               decalage= 20, retard= 0)
        self.Manager.addToTable(SQL_DB.LienTrajetsStation, id_trajets= 1, id_station= 9,
               decalage= 30, retard= 0)

    def fillStations(self):
        self.Manager.addToTable(SQL_DB.Station, nom= 'Ottignies', id_station= 6)
        self.Manager.addToTable(SQL_DB.Station, nom= 'Etterbeek', id_station= 7)
        self.Manager.addToTable(SQL_DB.Station, nom= 'Bxl-Luxembourg', id_station= 8)
        self.Manager.addToTable(SQL_DB.Station, nom= 'Bxl-Schuman', id_station= 9)

    def fillDB(self):
        print('Erasing DB before creating one')
        try:
            self.Manager.reset()
        except:
            print('No DB to reset, creating new one')
        self.createDB()
        self.reconnect()
        self.fillTrain()
        self.fillPC()
        self.fillTrajets()
        self.fillLienTrajetsStation()
        self.fillStations()


if __name__ == '__main__':
    test = Filler()
    test.fillDB()
