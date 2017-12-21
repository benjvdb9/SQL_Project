from DB_resuests import DB_Manager

class Filler()
    def __init__(self):
        self.Manager = DB_Manager()

    def fillTrain(self):
        self.Manager.addToTable()
