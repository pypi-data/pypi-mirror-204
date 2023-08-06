'''
Import Socket interface that the Server class is a child of
'''
from SocketInterface import SocketInterface

##############################
'''
Server Interface, contains methods that a server would need regardless of implementation, such as binding, and tracking the connection socket.
'''
class ServerInterface(SocketInterface):

    def __init__(self) -> None:
        super().__init__()
    
    '''
    Binds using the ip and port number. Should catch and OS error, and display the error, and 
    should return false.

    An input state must be flipped to true, to indicate that on a class level, that this object has recieved valid input
    '''
    def _bind_socket(self) -> bool:
        try:
            super().bind((self.ip, self.port_num))
        except OSError as e:
            print(f"Error {e.errno}: {e.strerror}")
            return False

        self.input_state = True
        return True
    
    '''
    The connection socket is tracked by the class through this method.
    '''
    def connect_to_client(self, connectionSocket):
        self.connectionSocket = connectionSocket