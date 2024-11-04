import client
import threading
import socket

HOST = '127.0.0.1'
PORT = 12345


client.username = input("Enter your username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def message_callback(message):
    print("Received message:", message)
    print("Received message:", message['message'])


threading.Thread(target=client.receive_messages, args=(client_socket,message_callback)).start()
threading.Thread(target=client.send_message, args=(client_socket,)).start()