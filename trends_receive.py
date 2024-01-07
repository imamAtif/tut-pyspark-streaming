import socket


def start_server():
    server_address = ("127.0.0.1", 5555)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(server_address)
        sock.listen(1)

        print(f"Server listening on {server_address}")

        while True:
            connection, client_address = sock.accept()
            print("Connection from", client_address)

            try:
                # Receive and print messages from the client continuously
                while True:
                    data = connection.recv(1024)
                    if not data:
                        break
                    print("Received:", data.decode("utf-8"))

            except ConnectionResetError:
                print("Client disconnected.")
            finally:
                connection.close()


if __name__ == "__main__":
    start_server()
