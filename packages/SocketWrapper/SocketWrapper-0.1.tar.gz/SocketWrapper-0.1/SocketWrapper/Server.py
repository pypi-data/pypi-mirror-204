'''
Import Server interface that the Server class is a child of
'''

from ServerInterface import ServerInterface

##############################
'''
Server class, child of Server interface. Used as a container for the collection of the server information and automatically
using that information.
'''
class Server(ServerInterface):
    def __init__(self, ip: str, port: str) -> None:
        super().__init__()
        self.ip = ip
        self.port_num = port

        self._parse_file()

    '''
    Runs as part of the initialization. Converts the port to a int. and then binds the socket.
    '''
    def _parse_file(self) -> None:
        if ((self._convert_port() == False) or (self._bind_socket() == False)):
            raise StopIteration
    
    '''
    Takes a msg and checks if it meets a requirement. If it does, false is returned.
    '''
    def check_end_condition(self, msg:str):
        if (msg == "exit"):
            self.send_msg(msg)
            self.connectionSocket.close()
            self.close()
            return False
        
        else:
            return True