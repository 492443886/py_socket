import socket
import threading
import json
import struct


username = ""


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

def receive_messages(client_socket, callback = None):
    """Continuously receive messages from the server."""
    while True:
        try:
            message = receive_full(client_socket)
            if message:
                data = json.loads(message)
                if callback:
                    callback(data)
                print(f"{data['username']}: {data['message']}")
        except Exception as e:
            print(f"Connection error: {e}")
            client_socket.close()
            break

def send_message(client_socket):
    """Send messages to the server."""
    while True:
        message = input()
        data = json.dumps({'username': username, 'message': message})
        send_full(client_socket, data.encode('utf-8'))


if __name__ == '__main__':  

    HOST = '127.0.0.1'
    PORT = 12345
    username = input("Enter your username: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    threading.Thread(target=send_message, args=(client_socket,)).start()
