"""This module provides a Client class for sending and receiving files."""
import argparse
import hashlib
import os
import socket


class Client:
    """Client class for sending and receiving files."""

    def __init__(self, host='127.0.0.1', port=9999, download_dir='downloads'):
        """
        Initialize a Client object.

        :param host: The hostname of the server
        :param port: The port number of the server
        :param download_dir: The directory where the requested files will be saved
        """
        self.host = host
        self.port = port
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    def calculate_hash(self, filepath):
        """
        Calculate the SHA-256 hash of a file.

        :param filepath: The path to the file for which the hash is to be calculated.
        :return: A hexadecimal string representing the SHA-256 hash of the file.
        """
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def request_file(self, filename):
        """
        Request a file from the server and save it locally.

        :param filename: The name of the file to request from the server.
        This method connects to the server using a socket, sends a request for the specified file,
        receives the file in chunks, and writes it to the local download directory. If the file size
        cannot be determined or an error occurs during the transfer, an error message is printed.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.send(f"GET {filename}\n".encode())

            file_size = client_socket.recv(20).decode().strip()
            if not file_size.isdigit():
                print("Error receiving the file:", file_size)
                return

            file_size = int(file_size)
            filepath = os.path.join(self.download_dir, filename)

            with open(filepath, "wb") as file:
                received = 0
                while received < file_size:
                    chunk = client_socket.recv(min(4096, file_size - received))
                    if not chunk:
                        break
                    file.write(chunk)
                    received += len(chunk)

            print(f"File {filename} downloaded successfully.")

    def update_file(self, filename):
        """
        Send an updated file to the server.

        :param filename: The name of the file to send to the server.
        This method connects to the server using a socket, sends an update for the specified file,
        sends the file in chunks, and waits for the server's response. If the file does not exist or
        an error occurs during the transfer, an error message is printed.
        """
        filepath = os.path.join(self.download_dir, filename)

        if not os.path.exists(filepath):
            print("Error: File not found for update.")
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))

            client_socket.send(f"UPDATE {filename}\n".encode())
            response = client_socket.recv(1024)
            if response != b"OK\n":
                print("Server did not accept the update")
                return

            with open(filepath, "rb") as file:
                for chunk in iter(lambda: file.read(4096), b""):
                    client_socket.send(chunk)

            client_socket.send(b"EOF")

            response = client_socket.recv(1024).decode().strip()
            print("Server response:", response)


def main():
    """
    Main entry point of the client program.

    This function parses the command line arguments and invokes either the request_file or
    update_file method of the Client class, depending on the argument provided.

    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=[
                        'request', 'update'], help="Action to be performed.")
    args = parser.parse_args()

    client = Client()

    if args.action == "request":
        client.request_file("test.txt")
    elif args.action == "update":
        client.update_file("test.txt")
    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()
