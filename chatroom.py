import socket
import threading
import sys

# TCP Server
class ServerTCP:
    def __init__(self, server_port):
        '''
        Initialize the TCP server, bind it to the given port, and set up the client dictionary,
        the socket handling, and event handling.
        '''
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((socket.gethostbyname(socket.gethostname()), self.server_port))
        self.server_socket.listen()
        self.clients = {}
        self.run_event = threading.Event()
        self.handle_event = threading.Event()

    def accept_client(self):
        '''
        Accept a new client connection, get their name, and broadcast their arrival.
        '''
        client_socket, client_addr = self.server_socket.accept()
        client_name = client_socket.recv(1024).decode('utf-8')
        # Check if the client name is taken
        if client_name in self.clients.values():
            client_socket.send("Name already taken".encode('utf-8'))
            return False
        else:
            # Welcome statements if name is not taken
            client_socket.send("Welcome".encode('utf-8'))
            self.clients[client_socket] = client_name
            print(f"{client_name} joined the chatroom")
            self.broadcast(client_socket, "join")
            return True

    def close_client(self, client_socket):
        '''
        Remove a client from the chatroom, delete them from the dictionary, and close their socket.
        '''
        if client_socket in self.clients:
            del self.clients[client_socket]
            client_socket.close()
            return True
        return False

    def broadcast(self, client_socket_sent, message):
        '''
        Broadcast a message to all connected clients, except the sender.
        '''
        client_name = self.clients[client_socket_sent]
        if message == 'join':
            broadcast_message = f"User {client_name} joined"
        elif message == 'exit':
            broadcast_message = f"User {client_name} left"
        else:
            broadcast_message = f"{client_name}: {message}"
        
        # Prevent message from being broadcasted to the sender
        for client_socket in self.clients:
            if client_socket != client_socket_sent:
                client_socket.send(broadcast_message.encode('utf-8'))

    def shutdown(self):
        '''
        Send a shutdown message to all clients, clear the run and handle events, and close the server.
        '''
        for client_socket in self.clients:
            client_socket.send("server-shutdown".encode('utf-8'))
            client_socket.close()
        self.run_event.clear()
        self.handle_event.clear()
        self.server_socket.close()

    def get_clients_number(self):
        '''
        Return the number of currently connected clients.
        '''
        return len(self.clients)
    
    def handle_client(self, client_socket):
        '''
        Continuously handle incoming messages from the client, and broadcast them. Check for exit message.
        '''
        while self.handle_event.is_set():
            try:
                message = client_socket.recv(1024).decode('utf-8')
                # Remove client if message is "exit"
                if message == 'exit':
                    self.broadcast(client_socket, 'exit')
                    self.close_client(client_socket)
                    break
                else:
                    self.broadcast(client_socket, message)
            except:
                break

    def run(self):
        '''
        Start the TCP server, accept new clients, and handle them in separate threads.
        '''
        self.run_event.set()
        self.handle_event.set()
        print(f"TCP CHATROOM running on port {self.server_port} with {self.get_clients_number()} clients connected.")
        print("Press CTRL+C to shutdown the server")
        while self.run_event.is_set():
            try:
                if self.accept_client():
                    client_socket = list(self.clients.keys())[-1]
                    threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            except KeyboardInterrupt:
                self.shutdown()

# TCP Client
class ClientTCP:
    def __init__(self, client_name, server_port):
        '''
        Initialize the TCP socket as the client's socket with the provided name and server port.
        '''
        self.server_addr = socket.gethostbyname(socket.gethostname())
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_port = server_port
        self.client_name = client_name
        self.exit_run = threading.Event()
        self.exit_receive = threading.Event()

    def connect_server(self):
        '''
        Connect client to the TCP server and send the client's name.
        '''
        try:
            self.client_socket.connect((self.server_addr, self.server_port))
            self.client_socket.send(self.client_name.encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')

            # Client successfully connected
            if response == "Welcome":
                print("Connected to the TCP chatroom.")
                print("Type 'exit' to leave.")
                return True
            # Client failed to connect
            else:
                print(response)
                return False
        except:
            return False

    def send(self, text):
        '''
        Send a message to the server.
        '''
        self.client_socket.send(text.encode('utf-8'))

    def receive(self):
        '''
        Continuously receive and display messages from the server.
        '''
        while not self.exit_receive.is_set():
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                # CHeck for the server-shutdown message
                if message == 'server-shutdown':
                    print("\nServer is shutting down...")
                    self.exit_run.set()
                    self.exit_receive.set()
                    break
                # Clear the rest of the message line
                sys.stdout.write(f"\r\033[K{message}\n")
                sys.stdout.flush()
                sys.stdout.write(f"{self.client_name}: ")
                sys.stdout.flush()
            except:
                break

    def run(self):
        '''
        Run the TCP client, allowing sending and receiving of messages.
        '''
        # Connect to the server
        if self.connect_server():
            self.exit_run.set()
            threading.Thread(target=self.receive).start()
            while self.exit_run.is_set():
                try:
                    text = input(f'{self.client_name}: ')
                    # Exit case
                    if text == 'exit':
                        self.send('exit')
                        self.exit_run.clear()
                        self.exit_receive.set()
                        break
                    # Text to be sent using send method
                    else:
                        self.send(text)
                except KeyboardInterrupt:
                    self.send('exit')
                    self.exit_run.clear()
                    self.exit_receive.set()
                    break
        self.client_socket.close()

# UDP Server
class ServerUDP:
    def __init__(self, server_port):
        '''
        Initialize the UDP server, bind it to the given port, and set up socket handling.
        '''
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((socket.gethostbyname(socket.gethostname()), self.server_port))
        self.clients = {}
        self.messages = []

    def accept_client(self, client_addr, message):
        '''
        Accept a new client connection, get their name, and broadcast their arrival.
        '''
        # Check if the client name is taken
        if message in self.clients.values():
            self.server_socket.sendto("Name already taken".encode('utf-8'), client_addr)
            return False
        else:   
            # Welcome statements if name is not taken
            self.server_socket.sendto("Welcome".encode('utf-8'), client_addr)
            self.clients[client_addr] = message
            self.messages.append((client_addr, f"User {message} joined"))
            self.broadcast()
            return True

    def close_client(self, client_addr):
        '''
        Remove a client from the chatroom, delete them from the dictionary, and broadcast the message
        '''
        if client_addr in self.clients:
            client_name = self.clients[client_addr]
            del self.clients[client_addr]
            self.messages.append((client_addr, f"User {client_name} left"))
            self.broadcast()
            return True
        return False

    def broadcast(self):
        '''
        Broadcast the latest message to all clients except the sender.
        '''
        if self.messages:
            client_addr, message = self.messages[-1]
            for addr in self.clients:
                # Don't send the message to the sender
                if addr != client_addr:
                    self.server_socket.sendto(message.encode('utf-8'), addr)

    def shutdown(self):
        '''
        Send a shutdown message to all clients and close the server.
        '''
        for addr in list(self.clients.keys()):
            self.server_socket.sendto("server-shutdown".encode('utf-8'), addr)
            self.close_client(addr)
        self.server_socket.close()

    def get_clients_number(self):
        '''
        Return the number of currently connected clients.
        '''
        return len(self.clients)

    def run(self):
        '''
        Run the UDP chatroom server, handling client connections and messages.
        '''
        print(f"UDP CHATROOM running on port {self.server_port} with {self.get_clients_number()} clients connected.")
        print("Press CTRL+C to shutdown the server")
        try:
            while True:
                data, client_addr = self.server_socket.recvfrom(1024)
                message = data.decode('utf-8')

                # Join case to accept the client
                if message.startswith("join:"):
                    client_name = message.split("join:")[1]
                    self.accept_client(client_addr, client_name)
                # Exit case to remove the client
                elif message == f"{self.clients.get(client_addr, '')}: exit":
                    self.close_client(client_addr)
                # Broadcase any other message
                else:
                    if client_addr in self.clients:
                        self.messages.append((client_addr, message))
                        self.broadcast()
        except KeyboardInterrupt:
            self.shutdown()

# UDP Client
class ClientUDP:
    def __init__(self, client_name, server_port):
        '''
        Initialize the UDP client using the client's socket with the provided name and server port.
        '''
        self.server_addr = socket.gethostbyname(socket.gethostname())
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_port = server_port
        self.client_name = client_name
        self.exit_run = threading.Event()
        self.exit_receive = threading.Event()

    def connect_server(self):
        '''
        Connect the client to the server and send the client name.
        '''
        try:
            join_message = f"join:{self.client_name}"
            self.client_socket.sendto(join_message.encode('utf-8'), (self.server_addr, self.server_port))

            data, _ = self.client_socket.recvfrom(1024)
            response = data.decode('utf-8')

            # Successful connection using the welcome method
            if response == "Welcome":
                print("Connected to the UDP chatroom.")
                print("Type 'exit' to leave.")
                return True
            # Failed connection
            else:
                return False
        except Exception as e:
            print(f"Error connecting to server: {e}")
            return False

    def send(self, text):
        '''
        Send the message to the server, including the client's name.
        '''
        message = f"{self.client_name}: {text}"
        self.client_socket.sendto(message.encode('utf-8'), (self.server_addr, self.server_port))

    def receive(self):
        '''
        Continuously listen for messages from the server and display them to the client.
        '''
        while not self.exit_receive.is_set():
            try:
                data, _ = self.client_socket.recvfrom(1024)
                message = data.decode('utf-8')

                # Check for server-shutdown message
                if message == 'server-shutdown':
                    print("\nServer is shutting down...")
                    self.exit_run.set()
                    self.exit_receive.set()
                    break

                # Clear the rest of the message line
                sys.stdout.write('\r\033[K')  # Clear the line before printing
                sys.stdout.write(f"{message}\n")
                sys.stdout.flush()
                sys.stdout.write(f"{self.client_name}: ")
                sys.stdout.flush()
            except:
                break

    def run(self):
        '''
        Run the UDP client, allowing sending and receiving of messages.
        '''
        # Connect to the server
        if self.connect_server():
            self.exit_run.set()
            receive_thread = threading.Thread(target=self.receive)
            receive_thread.start()
            while self.exit_run.is_set():
                try:
                    text = input(f'{self.client_name}: ')
                    # Exit case
                    if text == 'exit':
                        self.send('exit')
                        self.exit_run.clear()
                        self.exit_receive.set()
                        receive_thread.join()
                        break
                    # Text to be sent using send method
                    else:
                        self.send(text)
                except KeyboardInterrupt:
                    self.send('exit')
                    self.exit_run.clear()
                    self.exit_receive.set()
                    receive_thread.join()
                    break
        self.client_socket.close()