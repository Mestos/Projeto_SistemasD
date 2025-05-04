import socket
import threading
import time

clientes_provedores = []
clientes_receptores = []

lock = threading.Lock()

def handle_client(conn, addr):
    print(f"Conexão de {addr}")
    conn.send("Você é provedor (0) ou receptor (1)?".encode())

    tipo = conn.recv(1024).decode().strip()

    while tipo not in ["0", "1"]:
        conn.send("Tipo inválido. Digite 0 para provedor ou 1 para receptor:".encode())
        tipo = conn.recv(1024).decode().strip()

    conn.send("Aprovado".encode())

    if tipo == "0":
        with lock:
            clientes_provedores.append(conn)
        print(f"Provedor conectado: {addr}")

        while True:                             #Checagem de conexão
            try:                                
                conn.send("0".encode())         #Mensagem para checar conexão
                # Espera uma equação de um receptor
                r = conn.recv(1024).decode()    #Confirmação do provedor
                if r == "0":                    #Provedor confirma que a conexão ainda está ativa
                    time.sleep(5.5)             #Tempo de espera entre o envio das mensagens de confirmação
                    continue
                else:
                    print("Mensagem irregular\n")
                    break
            except ConnectionResetError:        #Conexão foi fechada pelo provedor
                    print("Conexão fechada pelo outro lado (ConnectionResetError).")
                    break
            except Exception as e: 
                print(f"Thread do provedor: {e} \n")
                break
        clientes_provedores.remove(conn)        #Remoção do provedor da lista assim que a conexão acaba

    elif tipo == "1":
        with lock:
            clientes_receptores.append(conn)
        print(f"Receptor conectado: {addr}")
        eq = conn.recv(1024).decode()

        # Envia para o primeiro provedor disponível
        with lock:
            if clientes_provedores:
                while True:
                    try:
                        # Envia a equação para o provedor
                        provedor = clientes_provedores.pop(0)
                        provedor.send(eq.encode())
                        resposta = provedor.recv(1024).decode()
                        conn.send(resposta.encode())
                        # Devolve o provedor para a lista
                        clientes_provedores.append(provedor)
                        break
                    except BrokenPipeError:
                        print("Conexão fechada pelo outro lado (BrokenPipeError).")
                        break
                    except ConnectionResetError:
                        print("Conexão fechada pelo outro lado (ConnectionResetError).")
                        break
                    except Exception as e:
                        print(f"Erro ao enviar dados: {e}")
                        break
            else:
                conn.send("Nenhum provedor disponível no momento.".encode())
                
    print(f"Conexão com {addr} Fechada \n") 
    conn.close()


def main():
    host = '127.0.0.1'
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor escutando em {host}:{port}...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == '__main__':
    main()
