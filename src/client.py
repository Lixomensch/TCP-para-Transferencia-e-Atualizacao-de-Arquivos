import argparse
import hashlib
import os
import socket
import time


class Client:
    def __init__(self, host='127.0.0.1', port=9999, download_dir='tests'):
        self.host = host
        self.port = port
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    def calcular_hash(self, filepath):
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def solicitar_arquivo(self, filename):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.host, self.port))
            client.send(f"GET {filename}\n".encode())

            file_size = client.recv(20).decode().strip()
            if not file_size.isdigit():
                print("Erro ao receber o arquivo:", file_size)
                return

            file_size = int(file_size)
            filepath = os.path.join(self.download_dir, filename)

            with open(filepath, "wb") as f:
                received = 0
                while received < file_size:
                    chunk = client.recv(min(4096, file_size - received))
                    if not chunk:
                        break
                    f.write(chunk)
                    received += len(chunk)

            print(f"Arquivo {filename} baixado com sucesso.")

    def atualizar_arquivo(self, filename):
        filepath = os.path.join(self.download_dir, filename)
        
        if not os.path.exists(filepath):
            print("Erro: Arquivo não encontrado para atualização.")
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.host, self.port))

            client.send(f"UPDATE {filename}\n".encode())
            time.sleep(1)
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    client.send(chunk)
                    print(f"Enviando chunk: {chunk[:50]}...")
            client.send(b"EOF")

            response = client.recv(1024).decode().strip()
            print("Resposta do servidor:", response)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['request', 'update'], help="Ação a ser realizada.")
    args = parser.parse_args()

    client = Client()

    if args.action == "request":
        client.solicitar_arquivo("test.txt")
    elif args.action == "update":
        client.atualizar_arquivo("test.txt")
    else:
        print("Opção inválida.")


if __name__ == "__main__":
    main()
