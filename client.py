#vim client.py

import socket
import threading

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.joined_room = None
        self.username = None

    def start(self):
        self.sock.connect((self.host, self.port))
        self.username = input("Enter your username: ")
        print(f"Connected to server as '{self.username}'")

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        while True:
            user_input = input("Type '/options' to see available options or type a message: ")

            if user_input.lower() == "/options":
                self.show_options()
            elif user_input in ["1", "2", "3"]:
                if user_input == "1":
                    self.list_chat_rooms()
                elif user_input == "2":
                    room_id = input("Enter a new chat room ID: ")
                    self.create_chat_room(room_id)
                elif user_input == "3":
                    room_id = input("Enter the chat room ID to join: ")
                    self.join_chat_room(room_id)
            elif user_input.lower() == "quit":
                if self.joined_room:
                    self.leave_chat_room()
                else:
                    print("You are not in any chat room.")
            else:
                if self.joined_room:
                    self.send_message(user_input)
                else:
                    print("Invalid command. Try again.")

    def show_options(self):
        print("Options:")
        print("1. List all chat rooms")
        print("2. Create a new chat room")
        print("3. Join an existing chat room")
        if self.joined_room:
            print("Type 'quit' to leave the chat room")

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                print(data.decode())
            except socket.error:
                break

    def create_chat_room(self, room_id):
        self.sock.send(f"/create {room_id} {self.username}".encode())
        self.joined_room = room_id

    def join_chat_room(self, room_id):
        self.sock.send(f"/join {room_id} {self.username}".encode())
        self.joined_room = room_id

    def leave_chat_room(self):
        self.sock.send("/leave".encode())
        print(f"Left chat room '{self.joined_room}'.")
        self.joined_room = None

    def list_chat_rooms(self):
        self.sock.send("/list".encode())

    def send_message(self, message):
        self.sock.send(f"{self.joined_room}:{self.username}: {message}".encode())

if __name__ == "__main__":
    client = ChatClient('65.0.130.62', 6000)
    client.start()