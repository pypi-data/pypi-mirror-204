'''
Import the ClientInterface that the Client class is a child of the Client Interface
'''

from interfaces.ClientInterface import ClientInterface

##############################

class Client(ClientInterface):
    '''
    Client class, child of ClientInterface. Used as a container for the collection of the client information and automatically
    using that information.

    Constructing this with no arguments will default both to '', which whill cause the ip to point to the loopback, and the 
    port to default to 12000.
    '''
    def __init__(self, ip: str = '', port: str = '') -> None:
        super().__init__()
        self.ip = ip
        self.port_num = port
        self.connectionSocket = self

        self._parse_file()
    
    def _parse_file(self) -> None:
        '''
        Runs as part of the initialization. Converts the port to a int. and then binds the socket.
        '''
        if ((self._convert_port() == False) or (self._connect_socket() == False)):
            raise StopIteration
    
    def check_end_condition(self, msg:str):
        '''
        Takes a msg and checks if it meets a requirement. If it does, false is returned.
        '''
        if (msg == "exit"):
            self.send_msg(msg)
            self.connectionSocket.close()

            return False
        
        else:
            return True
