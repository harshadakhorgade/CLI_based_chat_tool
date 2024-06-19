#server.py
import socket
import threading
from pymongo import MongoClient

class ChatRoom:
    def __init__(self, room_id, db):
        self.room_id = room_id
        self.clients = []
        self.messages = []
        self.db = db

    def add_client(self, client_socket):
        self.clients.append(client_socket)

    def remove_client(self, client_socket):
        self.clients.remove(client_socket)

    def broadcast(self, sender_socket, message):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode())
                except socket.error as e:
                    print(f"Error broadcasting message to a client: {e}")
                    self.remove_client(client)

        # Save the message to MongoDB
        self.messages.append(message)
        self.db[self.room_id].insert_one({'message': message})

class ChatServer:
    def __init__(self, host, port, mongo_host='0.0.0.0', mongo_port=27017):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.client = MongoClient(f'mongodb://{self.mongo_host}:{self.mongo_port}/')
        self.db = self.client['chat_server']
        self.chat_rooms = {}

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, address = self.sock.accept()
            print(f"Accepted connection from {address}")

            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        self.send_options(client_socket)

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode()

                if message.startswith("/"):
                    self.handle_command(client_socket, message)
                else:
                    self.handle_chat(client_socket, message)

            except socket.error as e:
                print(f"Error receiving data from client: {e}")
                break

        print(f"Connection closed.")
        client_socket.close()

    def send_options(self, client_socket):
        options = "Options:\n1. /list - List all chat rooms\n2. /create - Create a new chat room\n3. /join - Join an existing chat room\n"
        client_socket.send(options.encode())

    def handle_command(self, client_socket, command):
        parts = command.split()
        if len(parts) == 3:
            action = parts[0][1:].lower()
            room_id = parts[1]
            username = parts[2]

            if action == "create":
                self.create_chat_room(client_socket, room_id, username)
            elif action == "join":
                self.join_chat_room(client_socket, room_id, username)
            else:
                client_socket.send("Invalid command. Try again.".encode())
        elif command.strip().lower() == "/list":
            self.list_chat_rooms(client_socket)
        else:
            client_socket.send("Invalid command. Try again.".encode())

    def create_chat_room(self, client_socket, room_id, username):
        if room_id not in self.chat_rooms:
            chat_room = ChatRoom(room_id, self.db)
            chat_room.add_client(client_socket)
            self.chat_rooms[room_id] = chat_room
            welcome_message = f"Welcome to the chat room '{room_id}', {username}!"
            client_socket.send(welcome_message.encode())
        else:
            client_socket.send(f"Chat room '{room_id}' already exists. Choose another room ID.".encode())

    def join_chat_room(self, client_socket, room_id, username):
        if room_id in self.chat_rooms:
            self.chat_rooms[room_id].add_client(client_socket)
            welcome_message = f"Welcome to the chat room '{room_id}', {username}!"
            client_socket.send(welcome_message.encode())
        else:
            client_socket.send(f"Chat room '{room_id}' does not exist. Create it or choose another room ID.".encode())

    def list_chat_rooms(self, client_socket):
        rooms = "Available chat rooms:\n" + "\n".join(self.chat_rooms.keys())
        client_socket.send(rooms.encode())

    def handle_chat(self, client_socket, message):
        for chat_room in self.chat_rooms.values():
            if client_socket in chat_room.clients:
                chat_room.broadcast(client_socket, message)

if __name__ == "__main__":
    server = ChatServer('0.0.0.0', 6000)
    server.start()


