from DB_requests import DB_Manager

class Interpreter():
    def __init__(self):
        self.state = 'running'
        self.command = ''
        self.manager = DB_Manager()

    def interpret(self):
        self.command = input('commande?\n')

        if self.command == 'trajet':
            id_trajet = input('ID de trajet?\n')
            self.manager.selectTrajets(id_trajet)

        elif self.command == 'info':
            id_trajet = input('ID de trajet?\n')
            self.manager.getTrainInfo(id_trajet)

        elif self.command == 'station':
            id_station = input('Station?\n')
            self.manager.getStationInfo(id_station)
            
        elif self.command == 'quit':
            self.state = 'stopped'
            
        else:
            print('Commande non reconnue\n')

if __name__ == '__main__':
    inter = Interpreter()
    while inter.state == 'running':
        inter.interpret()

    print('Exiting code')
