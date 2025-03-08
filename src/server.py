import hashlib
import os
import socket
import threading


class Server:
    def __init__(self, host='0.0.0.0', port=5000, files_dir='data'):
        self.host = host
        self.port = port
        self.files_dir = files_dir
        self.setup_server()

    def setup_server(self):
        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Servidor rodando em {self.host}:{self.port}")

    def calcular_hash(self, filepath):
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
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

        if os.path.exists(filepath):
            hash_atual = self.calcular_hash(filepath)
            conn.send(f"OK {hash_atual}\n".encode())
            with open(filepath, "rb") as f:
                conn.sendfile(f)
        else:
            conn.send("ERRO Arquivo não encontrado\n".encode())

    def handle_update(self, conn, args):
        filename = args[0]
        filepath = os.path.join(self.files_dir, filename)

        with open(filepath, "wb") as f:
            while chunk := conn.recv(4096):
                f.write(chunk)

        novo_hash = self.calcular_hash(filepath)
        print(f"Arquivo {filename} atualizado. Hash: {novo_hash}")
        conn.send(f"OK {novo_hash}\n".encode())

    def start(self):
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.handle_client,
                             args=(conn, addr)).start()


if __name__ == "__main__":
    server = Server()
    server.start()
