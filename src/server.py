"""This module provides a Server class for handling client connections and file transfers."""
import hashlib
import os
import socket
import threading


class Server:
    """Server class for handling client connections and file transfers."""

    def __init__(self, host='0.0.0.0', port=9999, files_dir='data'):
        """
        Initialize a Server object.

        :param host: The hostname of the server (default='0.0.0.0')
        :param port: The port number of the server (default=9999)
        :param files_dir: The directory where the files will be saved (default='files')
        """
        self.host = host
        self.port = port
        self.files_dir = files_dir
        self.setup_server()

    def setup_server(self):
        """
        Create the server socket, bind it to the specified host and port, and start listening.

        :return: None
        """
        os.makedirs(self.files_dir, exist_ok=True)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server running on {self.host}:{self.port}")

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

    def handle_client(self, conn, addr):
        """
        Handle communication with a connected client.
        """
        print(f"Client connected: {addr}")
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break

                command, *args = data.split()

                if command == "GET":
                    self.handle_get(conn, args)
                elif command == "UPDATE":
                    self.handle_update(conn, args)
                elif command == "NEW":
                    self.handle_new(conn, args)
        except Exception as e:
            print(f"Error with client {addr}: {e}")
        finally:
            conn.close()
            print(f"Client {addr} disconnected.")

    def handle_get(self, conn, args):
        """
        Handle a GET request from a client.

        :param conn: The socket connection to the client.
        :param args: A list containing the filename requested by the client.
        This method sends the requested file to the client in chunks, prefixing the
        data with the file size as a 20-digit zero-padded decimal number. If the file
        does not exist, an error message is sent to the client instead.
        """
        filename = args[0]
        filepath = os.path.join(self.files_dir, filename)

        if not os.path.exists(filepath):
            conn.send(b"ERROR: File not found\n")
            return

        file_size = os.path.getsize(filepath)
        conn.send(f"{file_size:020d}".encode())
        with open(filepath, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                conn.send(chunk)

        print(f"File {filename} sent to client {conn.getpeername()}")

    def handle_update(self, conn, args):
        """
        Handle an UPDATE request from a client.

        :param conn: The socket connection to the client.
        :param args: A list containing the filename requested by the client.
        This method writes the file received from the client to the server's
        data directory, checks the integrity of the received file using SHA-256
        and sends the hash to the client. If an error occurs during the transfer
        or the file does not exist, an error message is sent to the client instead.
        """
        filename = args[0]
        filepath = os.path.join(self.files_dir, filename)

        conn.send(b"OK\n")

        with open(filepath, "wb") as file:
            while True: 
                chunk = conn.recv(4096)
                if not chunk or chunk.endswith(b"EOF"):
                    file.write(chunk[:-3])
                    break
                file.write(chunk)

        conn.send(b"OK\n")

        new_hash = self.calculate_hash(filepath)
        print(f"File {filename} updated. Hash: {new_hash}")
        conn.send(f"OK {new_hash}\n".encode())

    def handle_new(self, conn, args):
        """
        Handle a NEW request from a client.
        
        :param conn: The socket connection to the client.
        :param args: A list containing the filename to be stored.
        """
        filename = args[0]
        filepath = os.path.join(self.files_dir, filename)

        conn.send(b"OK\n")
        with open(filepath, "wb") as file:
            while True: 
                chunk = conn.recv(4096)
                if not chunk or chunk.endswith(b"EOF"):
                    file.write(chunk[:-3])
                    break
                file.write(chunk)

        conn.send(b"File stored successfully\n")
        print(f"New file {filename} received and stored.")

    def start(self):
        """
        Start the server and listen for incoming connections.

        This method enters an infinite loop where it waits for incoming connections
        and starts a new thread to handle each one. The main thread continues to listen
        for new connections.

        :return: None
        """
        while True:
            conn, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client,
                             args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    server = Server()
    server.start()
