'''
Import the ClientInterface that the Client class is a child of
'''

from interfaces.ClientInterface import ClientInterface

##############################

'''
Client class, child of ClientInterface. Used as a container for the collection of the client information and automatically
using that information.
'''
class Client(ClientInterface):
    def __init__(self, ip: str, port: str) -> None:
        super().__init__()
        self.ip = ip
        self.port_num = port
        self.connectionSocket = self

        self._parse_file()
    
    '''
    Runs as part of the initialization. Converts the port to a int. and then binds the socket.
    '''
    def _parse_file(self) -> None:
        if ((self._convert_port() == False) or (self._connect_socket() == False)):
            raise StopIteration
    
    '''
    Takes a msg and checks if it meets a requirement. If it does, false is returned.
    '''
    def check_end_condition(self, msg:str):
        if (msg == "exit"):
            self.send_msg(msg)
            self.connectionSocket.close()

            return False
        
        else:
            return True
