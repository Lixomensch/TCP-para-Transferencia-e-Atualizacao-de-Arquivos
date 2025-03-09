import hashlib
import os
import socket
import threading


class Server:
    def __init__(self, host='0.0.0.0', port=9999, files_dir='data'):
        self.host = host
        self.port = port
        self.files_dir = files_dir
        self.setup_server()

    def setup_server(self):
        os.makedirs(self.files_dir, exist_ok=True)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Servidor rodando em {self.host}:{self.port}")

    def calcular_hash(self, filepath):
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def handle_client(self, conn, addr):
        print(f"Cliente conectado: {addr}")
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break

                comando, *args = data.split()

                if comando == "GET":
                    self.handle_get(conn, args)
                elif comando == "UPDATE":
                    self.handle_update(conn, args)
        except Exception as e:
            print(f"Erro com o cliente {addr}: {e}")
        finally:
            conn.close()
            print(f"Cliente {addr} desconectado.")

    def handle_get(self, conn, args):
        filename = args[0]
        filepath = os.path.join(self.files_dir, filename)

        if not os.path.exists(filepath):
            conn.send(b"ERROR: Arquivo nao encontrado\n")
            return

        file_size = os.path.getsize(filepath)
        conn.send(f"{file_size:020d}".encode())
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                conn.send(chunk)

        print(f"Arquivo {filename} enviado para o cliente {conn.getpeername()}")

    def handle_update(self, conn, args):
        filename = args[0]
        filepath = os.path.join(self.files_dir, filename)
        
        conn.send(b"OK\n")
        
        with open(filepath, "wb") as f:
            while chunk := conn.recv(4096):
                if not chunk or chunk == b"EOF":
                    break
                f.write(chunk)
        
        conn.send(b"OK\n")

        novo_hash = self.calcular_hash(filepath)
        print(f"Arquivo {filename} atualizado. Hash: {novo_hash}")
        conn.send(f"OK {novo_hash}\n".encode())

    def start(self):
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    server = Server()
    server.start()
