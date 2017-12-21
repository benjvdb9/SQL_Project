class Interpreter():
    def __init__(self):
        self.state = 'running'
        self.command = ''

    def interpret(self):
        self.command = input('Enter command:\n')

        if self.command == 'input':
            print('SUCCESS\n')
        elif self.command == 'quit':
            self.state = 'stopped'
        else:
            print('FAILURE\n')

if __name__ == '__main__':

    inter = Interpreter()
    while inter.state == 'running':
        inter.interpret()

    print('Exiting code')
