from socket import socket, AF_INET, SOCK_STREAM

'''
Socket interface. Clients and servers are build around a sockets, and thus this can serve as a 
parent class to clients and servers.
'''
class SocketInterface(socket):

    def __init__(self) -> None:
        super().__init__(AF_INET, SOCK_STREAM)
        self.input_state = False
        self.connectionSocket = None
        self.ip = None
        self.port_num = None

    '''
    Converts port that the socket was initialized with from a string to an int, or defaults the value if the input
    is an empty string.

    Should catch a TypeError if the type casting from str to int fails, and in the case of catching the type error
    should return false.
    '''
    def _convert_port(self) -> bool:
        if (self.port_num == ''): 
            self.port_num = 12000
        else: 
            try: 
                self.port_num = int(self.port_num)
            except ValueError as e:
                print(e.with_traceback())
                return False
            
            return True
        
    '''
    Recieves a message using the connection socket. First takes an int, which is the size of the message.
    Then it loops and recieves until it has the full message (comparing to the original length sent).

    If an error occurs, throws StopIteration
    '''
    def recv_msg(self) -> None:
        try:
            msg_recv = self.connectionSocket.recv(4)
            msg_len = int.from_bytes(msg_recv, byteorder='big')
            msg = b''
            while (len(msg) < msg_len):
                remaining = msg_len - len(msg)
                msg += self.connectionSocket.recv(remaining)
        except OSError as e:
            raise StopIteration

        return msg.decode()
    
    '''
    Encodes the size of the message to the message itself, sends the entire "packet" through
    its socket. If an error occurs, StopIteration is thrown.
    '''
    def send_msg(self, msg: str) -> None:
        try:
            msg = msg.encode()
            msg_len = len(msg)
            msg_len_bytes = msg_len.to_bytes(4, byteorder='big')

            response_packet = msg_len_bytes + msg
            self.connectionSocket.sendall(response_packet)
        except OSError:
            raise StopIteration
