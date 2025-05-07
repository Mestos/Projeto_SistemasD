import socket
import threading
import time

clientes_provedores = []
clientes_receptores = []

lock = threading.Lock()

def pos_menor_precedencia(expr):
    operadores_niveis = [
        ['+', '-'],        # Menor precedência
        ['*', '/', '//', '%'],
        ['**']             # Maior precedência
    ]

    # Função auxiliar para verificar se estamos fora de parênteses
    def fora_dos_parenteses(i):
        count = 0
        for j in range(i):
            if expr[j] == '(':
                count += 1
            elif expr[j] == ')':
                count -= 1
        return count == 0

    # Procurar do menor para o maior nível de precedência
    for operadores in operadores_niveis:
        i = len(expr) - 1
        while i >= 0:
            if not fora_dos_parenteses(i):
                i -= 1
                continue
            # Verifica operadores de 2 caracteres (como // e **)
            if i > 0 and expr[i-1:i+1] in operadores and fora_dos_parenteses(i-1):
                return i - 1
            elif expr[i] in operadores:
                return i
            i -= 1
    return -1  # Nenhum operador encontrado fora dos parênteses

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
                conn.send("c".encode())         #Mensagem para checar conexão
                # Espera uma equação de um receptor
                r = conn.recv(1024).decode()    #Confirmação do provedor
                if r == "c":                    #Provedor confirma que a conexão ainda está ativa
                    time.sleep(5.5)             #Tempo de espera entre o envio das mensagens de confirmação
                    continue
                else:
                    print("Fechando conexão com provedor...\n")
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
            n=len(clientes_provedores)
            
        if n>1:
            centro = pos_menor_precedencia(eq)  # Posição do operador de menor precedência   
            começo = eq[:centro]            # Parte antes do operador
            operador = ''
            if eq[centro:centro+2] in ['**']:  # Operadores de 2 caracteres
                operador = eq[centro:centro+2]
                fim = eq[centro+2:]          # Parte depois do operador
            else:
                operador = eq[centro]
                fim = eq[centro+1:]          # Parte depois do operador
            while True:
                    try:
                        # Envia a equação para o provedor
                        provedor1 = clientes_provedores.pop(0)
                        provedor1.send(começo.encode())
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
            while True:
                    try:
                        # Envia a equação para o provedor
                        provedor2 = clientes_provedores.pop(0)
                        provedor2.send(fim.encode())
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
            resposta1 = provedor1.recv(1024).decode()
            resposta2 = provedor2.recv(1024).decode()
            if operador=="**":
                resposta = str(float(resposta1) ** float(resposta2))
            elif operador == "/":
                resposta = str(float(resposta1) / float(resposta2))
            elif operador == "+": 
                resposta = str(float(resposta1) + float(resposta2))
            elif operador == "-":
                resposta = str(float(resposta1) - float(resposta2))
            elif operador == "*":
                resposta = str(float(resposta1) * float(resposta2))
            
            conn.send(resposta.encode())
            with lock:
                clientes_provedores.append(provedor1)
                clientes_provedores.append(provedor2)
        else:
            with lock:
                provedor = clientes_provedores.pop(0)
                while True:
                    try:
                        # Envia a equação para o provedor
                        provedor.send(eq.encode())
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

            resposta = provedor.recv(1024).decode()
            conn.send(resposta.encode())
            with lock:
                clientes_provedores.append(provedor)
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
