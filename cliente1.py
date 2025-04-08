import socket


def client_main_server():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # conecta-se ao servidor principal

    data = client_socket.recv(1024).decode()  # recebe mensagem do servidor perguntando tipo de cliente

    print('Received from server: ' + data)  # mostra a mensagem no terminal

    while data != "Aprovado": #
        tipo = input(" -> ")  # digita uma mensagem identificando seu tipo
        client_socket.send(tipo.encode()) # envia mensagem ao servidor principal
        data = client_socket.recv(1024).decode()  # recebe mensagem do servidor perguntando tipo de cliente ou aprovando a mensagem
        print('Received from server: ' + data)  # mostra a mensagem no terminal
        
    match = client_socket.recv(1024).decode()  # recebe mensagem do servidor contendo ip e porta do match
    print('Received from server: ' + match)  # mostra a mensagem no terminal
    info = [match, tipo]
    
    client_socket.close()  # fecha conexão com o servidor principal       
    return info

def client_server():
    user_socket = socket.socket()
        

if __name__ == '__main__':
    info = client_main_server()
    