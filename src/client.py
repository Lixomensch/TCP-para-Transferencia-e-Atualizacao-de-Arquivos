import argparse
import hashlib
import os
import socket


class Client:
    def __init__(self, host='127.0.0.1', port=5000, download_dir='tests'):
        self.host = host
        self.port = port
        self.download_dir = download_dir
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def calcular_hash(self, filepath):
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()

    def solicitar_arquivo(self, filename):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.settimeout(10)

                client.connect((self.host, self.port))
                client.send(f"GET {filename}".encode())
                response = client.recv(1024).decode().strip()

                if response.startswith("OK"):
                    _, hash_server = response.split()
                    filepath = os.path.join(self.download_dir, filename)

                    print(f"Iniciando o download do arquivo: {filename}")

                    with open(filepath, "wb") as f:
                        while True:
                            try:
                                chunk = client.recv(4096)
                                if not chunk:
                                    break
                                f.write(chunk)

                            except socket.timeout:
                                print(
                                    "Erro: Tempo de espera excedido. O servidor pode estar muito lento ou não responder.")
                                break
                            except Exception as e:
                                print(
                                    f"Ocorreu um erro enquanto recebia os dados: {e}")
                                break

                    print(f"Arquivo {filename} baixado com sucesso.")
                else:
                    print("Erro: Arquivo não encontrado no servidor.")

        except socket.error as e:
            print(f"Erro de conexão: {e}")
        except PermissionError:
            print(
                f"Erro: Permissão negada ao tentar gravar no diretório {self.download_dir}.")
        except FileNotFoundError:
            print(f"Erro: O diretório {self.download_dir} não foi encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    def atualizar_arquivo(self, filename):
        filepath = os.path.join(self.download_dir, filename)
        if not os.path.exists(filepath):
            print("Erro: Arquivo não encontrado para atualização.")
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.host, self.port))
            client.send(f"UPDATE {filename}".encode())
            with open(filepath, "rb") as f:
                while chunk := f.read(4096):
                    client.send(chunk)

            response = client.recv(1024).decode().strip()
            print(f"Resposta do servidor: {response}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=[
                        'request', 'update'], help="Ação a ser realizada.")

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
