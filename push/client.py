import socket
import threading

HOST = "127.0.0.1"
PORT = 50000


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)

            if not data:
                print("Server disconnected.")
                break

            print(data.decode(), end="")

        except ConnectionResetError:
            print("Connection lost.")
            break


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        sock.connect((HOST, PORT))

        print("Connected to server.")
        print("Type a message and press Enter.")

        # Thread responsible for receiving messages
        receive_thread = threading.Thread(
            target=receive_messages,
            args=(sock,),
            daemon=True
        )

        receive_thread.start()

        while True:
            message = input()

            if message.lower() == "quit":
                break

            sock.sendall(message.encode())


if __name__ == "__main__":
    start_client()