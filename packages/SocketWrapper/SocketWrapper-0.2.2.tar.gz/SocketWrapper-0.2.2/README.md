# SocketWrapper

This project contains two classes: A client, and a server class. The goal is to abstract on the process of setting up clients and servers.
You can simply create a client, and a server, feeding both an IP and a port. The objects will use that information to set up sockets, and for the server, bind to a socket.

Both the server and client have error checking, which throw errors in the case of invalid input for the IP or Port.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Technologies](#technologies)
- [TODO](#todo)

## Installation

To use the SocketWrapper Package, follow the steps below:

1. Import the package using: `pip install SocketWrapper`
2. Import Client from Client.py: `from SocketWrapper.Client import Client`
3. Import Server from Server.py `from SocketWrapper.Server import Server` 

## Usage

Once you have installed SocketWrapper, you can use it to create server and client objects. You can do this by following the steps below:

1. new_client = Client(ip, port)

2. new_server = Server(ip, port)

## Technologies

SockerWrapper was developed using the following technologies:

- Python
- socket library
- os library

## TODO
- Create custom exceptions
- Create default constructors (optional \__init__ parameters)
- Create tests
- Add more functionality
- Add more detail to the methods and classes of input and output

## License

SocketWrapper is open source software licensed under the [MIT License](https://opensource.org/licenses/MIT).






