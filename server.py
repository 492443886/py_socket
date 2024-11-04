import socket
import threading
import json
import struct

HOST = '127.0.0.1'
PORT = 12345
clients = []

def send_full(client_socket, message):
    """Send a complete message with length prefix."""
    message_length = struct.pack('>I', len(message))  # 4-byte length prefix
    client_socket.sendall(message_length + message)

def receive_full(client_socket):
    """Receive a complete message based on the length prefix."""
    raw_length = client_socket.recv(4)
    if not raw_length:
        return None
    message_length = struct.unpack('>I', raw_length)[0]
    data = b''
    while len(data) < message_length:
        packet = client_socket.recv(message_length - len(data))
        if not packet:
            return None
        data += packet
    return data.decode('utf-8')

def broadcast(message, sender_socket):
    """Broadcast message to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                send_full(client, message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {e}")

def handle_client(client_socket):
    """Handle communication with a client."""
    while True:
        try:
            message = receive_full(client_socket)
            if message:
                print("Received:", message)
                data = json.loads(message)
                print(f"{data['username']}: {data['message']}")
                broadcast(message, client_socket)
        except Exception as e:
            print(f"Client disconnected: {e}")
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    """Start the server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Server started, waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"New connection from {addr}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

start_server()
