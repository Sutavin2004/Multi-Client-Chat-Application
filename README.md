# Python Multi-Client Chatroom (TCP & UDP)

# Overview
Python Multi-Client Chatroom is a real-time communication system that allows multiple clients to chat over both **TCP (connection-oriented)** and **UDP (connectionless)** protocols. The system includes a **multi-threaded TCP server** and a **UDP server** that handle multiple clients concurrently. This project demonstrates **network programming, multi-threading, and concurrent client handling**.

By implementing **Python sockets**, **threading**, and **event handling**, this chatroom enables seamless messaging, message broadcasting, and proper client session management.

# Features

### Multi-Client Chat Support
- Allows multiple clients to connect to a central chatroom.
- Supports **both TCP and UDP chatrooms**.

### Threaded TCP Server
- Handles multiple clients simultaneously using **multi-threading**.
- Manages client connections and broadcasts messages to all users.

### UDP Chatroom
- Uses UDP sockets to allow lightweight, fast messaging without persistent connections.
- Broadcasts messages to all connected users.

### Message Broadcasting
- Messages from one client are broadcasted to all other connected clients.

### Username Authentication
- Prevents duplicate usernames in the chatroom.

### Graceful Exit Handling
- Clients can disconnect cleanly without affecting other users.
- Server shutdown notifies all clients.

# Technology Stack

### Programming Language
- **Python 3.x**: Primary language for server and client implementation.

### Libraries and Frameworks
- **Sockets (TCP & UDP)**: Handles real-time communication.
- **Threading**: Manages multiple clients efficiently.
- **sys & argparse**: Enables command-line arguments and input handling.

# Installation

### Clone the Repository
```bash
git clone https://github.com/Sutavin2004/Python-Chatroom.git
cd Python-Chatroom
```

## Install Dependencies
No external dependencies are required, as this project only uses Python's built-in modules.

# Usage
### Running the TCP Server
Start the TCP server on port 12345:

```bash
python chatroom.py --server-tcp 12345
```
### Running TCP Clients
Each client must specify a username when connecting:

```bash
python client.py --name "User1"
```
To start multiple clients, run:

```bash
python client.py --name "User2"
python client.py --name "User3"
```
## Running the UDP Server
Start the UDP server on port 12345:

```bash
python server.py
```
### Running UDP Clients
Each client must specify a username when connecting:

```bash
python client.py --name "User1"
```
# Example Input and Output
### TCP Chat Example:
``` makefile
User1: Hello everyone!
User2: Hi User1!
User3: How’s it going?
```
### UDP Chat Example:
```vbnet
User1: Hey, this is a UDP chatroom!
User2: Cool, I'm in too!
User3: Let's chat!
```
# Challenges and Solutions
### Handling Multiple Clients Concurrently
Issue: Managing multiple client connections in TCP without affecting performance.
Solution: Implemented a multi-threaded server, where each client runs on a separate thread.

### Message Broadcasting
Issue: Messages needed to be broadcasted to all connected clients except the sender.
Solution: Used a dictionary to track clients and send messages only to non-sender sockets.

### UDP Reliability
Issue: UDP does not guarantee message delivery.
Solution: Implemented a system where messages are broadcasted multiple times to improve delivery chances.

# Contributions
Contributions are welcome! Follow these steps:

### Fork the Repository
### Create a Feature Branch
``` bash
git checkout -b feature-name
```
### Commit Your Changes
``` bash
git commit -m "Add new feature"
```
### Push the Branch
```bash
git push origin feature-name
```
### Open a Pull Request
# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Future Enhancements
Add a GUI interface using Tkinter or PyQt.
Implement private messaging between users.
Store chat history in a database.
Add encryption for secure messaging.
# Contact
Email: sutavin2004@gmail.com
